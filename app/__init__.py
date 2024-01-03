from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from app.custom_converters import ObjectIdConverter, CustomJSONEncoder
from flask_cors import CORS

app = Flask(__name__)
app.config.from_pyfile('../config.py')
jwt = JWTManager(app)

# Enable CORS for all routes
CORS(app, resources={r'/api/*': {'origins': '*'}})

# Register the custom converter
app.url_map.converters['ObjectId'] = ObjectIdConverter

app.json_encoder = CustomJSONEncoder

# MongoDB configuration
mongo = MongoClient(app.config['MONGO_URI'])
from app.routes import auth, notes, search
