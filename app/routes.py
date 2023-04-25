from flask import Blueprint, jsonify, abort, make_response
from .models.planet import Planet
from .models.moon import Moon

planets = [
    Planet(1, 'Earth', 'Home planet', 5),
    Planet(2, 'Mars', 'Fire planet', 4),
    Planet(3, 'Dune', 'Home of the freemen', 9)
]
moons = [
    Moon(1, "Sailor", planets[0]),
    Moon(2, "Orion", planets[0]),
    Moon(3, "Olivia", planets[1])
]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")
moons_bp = Blueprint("moons", __name__, url_prefix="/moons")

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message": f"Planet {planet_id} is not valid."}, 400))

    for planet in planets:
        if planet_id == planet.id:
            return planet
    
    abort(make_response({"message": "Planet {planet_id} is not found"}, 404))


@planets_bp.route("", methods=["GET"])
def handle_planets():
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

def validate_moon(moon_id):
    try:
        moon_id = int(moon_id)
    except:
        abort(make_response({"message": f"Moon {moon_id} is not valid."}, 400))

    for moon in moons:
        if moon_id == moon.id:
            return moon
    
    abort(make_response({"message": "Moon {moon_id} is not found"}, 404))


@moons_bp.route("", methods=["GET"])
def handle_moons():
    moon_response = []
    for moon in moons:
        moon_response.append({
            "id": moon.id,
            "name": moon.name,
            "planet": moon.planet
        })
    return str(moon_response)

@moons_bp.route("/<moon_id>", methods=["GET"])
def handle_moon(moon_id):
    moon = validate_moon(moon_id)

    return jsonify({
        "id": moon.id, 
        "name": moon.name,
        "planet": moon.planet
    })