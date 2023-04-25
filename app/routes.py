from flask import Blueprint, jsonify
from .models.planet import Planet

planets = [
    Planet(1, 'Earth', 'Home planet', 5),
    Planet(2, 'Mars', 'Fire planet', 4),
    Planet(3, 'Dune', 'Home of the freemen', 9)
]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

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

