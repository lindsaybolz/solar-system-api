from flask import Blueprint, jsonify, abort, make_response, request
from app.models.moon import Moon
from app import db


moons_bp = Blueprint("moons", __name__, url_prefix="/moons")

# helper function

def validate_moon(moon_id):
    try:
        moon_id = int(moon_id)
    except:
        abort(make_response({"message": f"Moon {moon_id} is not valid."}, 400))

    moon = Moon.query.get(moon_id)
    if not moon:
        abort(make_response({"message": f"Moon {moon_id} is not found"}, 404))

    return moon


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

