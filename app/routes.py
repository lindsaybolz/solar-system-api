from flask import Blueprint, jsonify, abort, make_response, request
from .models.planet import Planet
from .models.moon import Moon
from app import db

# planets = [
#     Planet(1, 'Earth', 'Home planet', 5),
#     Planet(2, 'Mars', 'Fire planet', 4),
#     Planet(3, 'Dune', 'Home of the freemen', 9)
# ]
# moons = [
#     Moon(1, "Sailor", planets[0]),
#     Moon(2, "Orion", planets[0]),
#     Moon(3, "Olivia", planets[1])
# ]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")
moons_bp = Blueprint("moons", __name__, url_prefix="/moons")

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message": f"Planet {planet_id} is not valid."}, 400))

    planet = Planet.query.get(planet_id)
    if not planet:   
        abort(make_response({"message": f"Planet {planet_id} is not found"}, 404))
    return planet

@planets_bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()
    new_planet = Planet(name=request_body["name"], 
                        description=request_body["description"],
                        mass=request_body["mass"])
    db.session.add(new_planet)
    db.session.commit()
    return make_response(f"Planet {new_planet.id} successfully created.")

@moons_bp.route("", methods=["POST"])
def create_moon():
    request_body = request.get_json()
    new_moon = Moon(name=request_body["name"], 
                        planet_id=request_body["planet_id"])
    
    db.session.add(new_moon)
    db.session.commit()
    return make_response(f"Moon {new_moon.id} successfully created.")

@planets_bp.route("", methods=["GET"])
def handle_planets():
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

@planets_bp.route("/<planet_id>", methods=["GET"])
def handle_planet(planet_id):
    planet = validate_planet(planet_id)

    return {
        "id": planet.id, 
        "name": planet.name,
        "description": planet.description,
        "mass": planet.mass
    }

@planets_bp.route('/<planet_id>', methods=["PUT"])
def update_planet(planet_id):
    request_body = request.get_json()
    planet = validate_planet(planet_id)

    planet.name = request_body['name']
    planet.description = request_body['description']
    planet.mass = request_body['mass']

    db.session.commit()

    return {"message": f"Planet {planet_id} successfully updated."}, 200

@planets_bp.route('/<planet_id>', methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return {"message": f"Planet {planet_id} successfully deleted."}, 200



def validate_moon(moon_id):
    try:
        moon_id = int(moon_id)
    except:
        abort(make_response({"message": f"Moon {moon_id} is not valid."}, 400))

    moon = Moon.query.get(moon_id)
    if not moon:
        abort(make_response({"message": f"Moon {moon_id} is not found"}, 404))

    return moon

@moons_bp.route("", methods=["GET"])
def handle_moons():
    moon_response = []
    moons = Moon.query.all()

    for moon in moons:
        moon_response.append({
            "id": moon.id,
            "name": moon.name,
            "planet": str(moon.planet)
        })
    return str(moon_response)

@moons_bp.route("/<moon_id>", methods=["GET"])
def handle_moon(moon_id):
    moon = validate_moon(moon_id)

    return jsonify({
        "id": moon.id, 
        "name": moon.name,
        "planet": str(moon.planet)
    })

@moons_bp.route('/<moon_id>', methods=["PUT"])
def update_moon(moon_id):
    request_body = request.get_json()
    moon = validate_moon(moon_id)

    moon.name = request_body['name']
    moon.planet_id = request_body['planet_id']

    db.session.commit()

    return {"message": f"Moon {moon_id} successfully updated."}, 200


@moons_bp.route('/<moon_id>', methods=["DELETE"])
def delete_moon(moon_id):
    moon = validate_moon(moon_id)

    db.session.delete(moon)
    db.session.commit()

    return {"message": f"Moon {moon_id} successfully deleted."}, 200

