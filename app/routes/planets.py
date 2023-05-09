from flask import Blueprint, jsonify, abort, make_response, request
from app.models.planet import Planet
from app.models.moon import Moon
from app import db

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

# helper function
def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message": f"Planet {planet_id} is not valid."}, 400))

    planet = Planet.query.get(planet_id)
    if not planet:   
        abort(make_response({"message": f"Planet {planet_id} is not found"}, 404))
    return planet

# planet routes
# route to create a planet
@planets_bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()
    new_planet = Planet(name=request_body["name"], 
                        description=request_body["description"],
                        mass=request_body["mass"])
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
        planet_response.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "mass": planet.mass
        })
    return jsonify(planet_response)

# route to get planet by ID
@planets_bp.route("/<planet_id>", methods=["GET"])
def handle_planet(planet_id):
    planet = validate_planet(planet_id)

    return {
        "id": planet.id, 
        "name": planet.name,
        "description": planet.description,
        "mass": planet.mass
    }

# route to update planet by ID
@planets_bp.route('/<planet_id>', methods=["PUT"])
def update_planet(planet_id):
    request_body = request.get_json()
    planet = validate_planet(planet_id)

    planet.name = request_body['name']
    planet.description = request_body['description']
    planet.mass = request_body['mass']

    db.session.commit()

    return {"message": f"Planet {planet_id} successfully updated."}, 200

# route to delete planet by ID
@planets_bp.route('/<planet_id>', methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return {"message": f"Planet {planet_id} successfully deleted."}, 200

# route to get all the moons of a planet by ID
@planets_bp.route('/<planet_id>/moons', methods=["GET"])
def get_moons(planet_id):
    planet = validate_planet(planet_id)

    moon_response = []
    for moon in planet.moons:
        moon_response.append(moon.to_dict())

    return jsonify(moon_response), 200

@planets_bp.route("/<planet_id>/moons", methods=["POST"])
def create_moons(planet_id):
    planet = validate_planet(planet_id)
    request_body = request.get_json()

    new_moon = Moon(name= request_body["name"], planet = planet)

    db.session.add(new_moon)
    db.session.commit()

    return jsonify(f"{new_moon.name} successfully created."), 201


