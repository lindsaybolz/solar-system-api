from flask import Blueprint, jsonify, abort, make_response, request
from .models.planet import Planet
from .models.moon import Moon
from app import db

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")
moons_bp = Blueprint("moons", __name__, url_prefix="/moons")

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

def validate_moon(moon_id):
    try:
        moon_id = int(moon_id)
    except:
        abort(make_response({"message": f"Moon {moon_id} is not valid."}, 400))

    moon = Moon.query.get(moon_id)
    if not moon:
        abort(make_response({"message": f"Moon {moon_id} is not found"}, 404))

    return moon

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
    return make_response(f"Planet {new_planet.id} successfully created.")

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

# moon routes
# route to create a moon
@moons_bp.route("", methods=["POST"])
def create_moon():
    request_body = request.get_json()
    new_moon = Moon(name=request_body["name"], 
                        planet_id=request_body["planet_id"])
    
    db.session.add(new_moon)
    db.session.commit()
    return make_response(f"Moon {new_moon.id} successfully created.")

# route to get all moons and by filter
@moons_bp.route("", methods=["GET"])
def handle_moons():
    name_query = request.args.get("name")
    if name_query:
        moons = Moon.query.filter_by(name=name_query)
    else:
        moons = Moon.query.all()
    moon_response = []
    
    for moon in moons:
        moon_response.append({
            "id": moon.id,
            "name": moon.name,
            "planet": str(moon.planet)
        })
    return str(moon_response)

# routes to get moon by ID
@moons_bp.route("/<moon_id>", methods=["GET"])
def handle_moon(moon_id):
    moon = validate_moon(moon_id)

    return jsonify({
        "id": moon.id, 
        "name": moon.name,
        "planet": str(moon.planet)
    })

# route to update a moon by ID
@moons_bp.route('/<moon_id>', methods=["PUT"])
def update_moon(moon_id):
    request_body = request.get_json()
    moon = validate_moon(moon_id)

    moon.name = request_body['name']
    moon.planet_id = request_body['planet_id']

    db.session.commit()

    return {"message": f"Moon {moon_id} successfully updated."}, 200

# route to delete moon by ID
@moons_bp.route('/<moon_id>', methods=["DELETE"])
def delete_moon(moon_id):
    moon = validate_moon(moon_id)

    db.session.delete(moon)
    db.session.commit()

    return {"message": f"Moon {moon_id} successfully deleted."}, 200

