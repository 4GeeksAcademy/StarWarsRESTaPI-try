"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorites
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/character', methods = ['GET'])
def get_character():
    character_info = Character.query.all()
    if character_info == []:
        return jsonify({"msg": "The character doesn't exist"}), 404
    result = list(map(lambda character: character.serialize(), character_info))
    return jsonify(result), 200

@app.route('/character/<int:id_character>')
def get_id_character(id_character):
    character_id = Character.query.filter_by(id = id_character).first()
    if character_id is None:
        return jsonify({"msg": "The character doesn't exist"}), 404
    return jsonify(character_id.serialize()), 200


@app.route('/planet', methods=['GET'])
def get_planet():
    planet_info = Planet.query.all() #acceder a la tabla planet y traer toda la info
    if planet_info == []:
        return jsonify({"msg": "The planet doesn't exist"}), 404
    result = list(map(lambda planet: planet.serialize(), planet_info))
    return jsonify(result), 200


@app.route('/planet/<int:id_planet>', methods=['GET'])
def get_id_planet(id_planet):
    planet_id = Planet.query.filter_by(id = id_planet).first()
    if planet_id is None:
        return jsonify({"msg": "The planet doesn't exist"}), 404 # cuando está vacio me transforma en un objeto
    return jsonify(planet_id.serialize()), 200
    
    


    




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
