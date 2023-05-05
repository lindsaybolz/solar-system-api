from flask import Blueprint, jsonify, abort, make_response, request
from app.models.planet import Planet
from app import db

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

# helper function
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is not valid."}, 400))

    model = cls.query.get(model_id)
    if not model:   
        abort(make_response({"message": f"{cls.__name__} {model_id} is not found"}, 404))
    
    return model

# planet routes
# route to create a planet
@planets_bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()
    if request_body.get('name') and request_body.get('description') and request_body.get('mass'):
        new_planet = Planet.from_dict(request_body)
    else:
        abort(make_response({"message": f"Planet input data incomplete.  Make sure you ahve a name, description and mass."}, 400))


    db.session.add(new_planet)
    db.session.commit()

    return jsonify(f"Planet {new_planet.id} successfully created."), 201

# route to get all planets and by filter
@planets_bp.route("", methods=["GET"])
def handle_planets():
    name_query = request.args.get("name")
    if name_query:
        planets = Planet.query.filter_by(name=name_query)
    else:
        planets = Planet.query.all()
    
    planet_response = []
    for planet in planets:
        planet_response.append(planet.to_dict())
    return jsonify(planet_response), 200

# route to get planet by ID
@planets_bp.route("/<planet_id>", methods=["GET"])
def handle_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    return planet.to_dict()

# route to update planet by ID
@planets_bp.route('/<planet_id>', methods=["PUT"])
def update_planet(planet_id):
    request_body = request.get_json()
    planet = validate_model(Planet, planet_id)

    planet.name = request_body['name']
    planet.description = request_body['description']
    planet.mass = request_body['mass']

    db.session.commit()

    return {"message": f"Planet {planet_id} successfully updated."}, 200

# route to delete planet by ID
@planets_bp.route('/<planet_id>', methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    db.session.delete(planet)
    db.session.commit()

    return {"message": f"Planet {planet_id} successfully deleted."}, 200

