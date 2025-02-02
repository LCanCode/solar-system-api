from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, abort, make_response, request

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(jsonify({"message":f"{cls.__name__} {model_id} invalid"}), 400))
    
    model = cls.query.get(model_id)
    if not model:
        abort(make_response(jsonify({"message":f"{cls.__name__} {model_id} not found"}), 404))

    return model



@planets_bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()
    new_planet = Planet.from_dict(request_body)
    db.session.add(new_planet)
    db.session.commit()

    return make_response(jsonify(f"Planet {new_planet.name} created successfully."), 201)

@planets_bp.route("", methods=["GET"])
def get_all_planets():
    planets = Planet.query.all()
    results = [planet.to_dict() for planet in planets]
    
    return jsonify(results)

@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    return planet.to_dict()

@planets_bp.route("/<planet_id>", methods=["PUT"])
def replace_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    planet_to_update = request.get_json()
    
    planet.name = planet_to_update["name"]
    planet.description = planet_to_update["description"]
    planet.solar_day = planet_to_update["solar_day"]

    db.session.commit()

    return make_response(jsonify(f"Planet {planet.name} updated successfully."))


@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet_to_delete = validate_model(Planet, planet_id)
    db.session.delete(planet_to_delete)
    db.session.commit()

    return make_response(jsonify(f"Planet {planet_to_delete.name} was deleted."))
