from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from app.custom_converters import ObjectIdConverter, CustomJSONEncoder
from flask_cors import CORS

app = Flask(__name__)
app.config.from_pyfile('../config.py')
jwt = JWTManager(app)

# Api limitter, IP Address based
limiter = Limiter(get_remote_address, app=app, storage_uri=app.config['REDIS_URI_FOR_RATELIMIT'])

# Enable CORS for all routes
CORS(app, resources={r'/api/*': {'origins': '*'}})

# Register the custom converter
app.url_map.converters['ObjectId'] = ObjectIdConverter

app.json_encoder = CustomJSONEncoder

# MongoDB configuration
mongo = MongoClient(app.config['MONGO_URI'])

from app.routes import auth, notes, search
