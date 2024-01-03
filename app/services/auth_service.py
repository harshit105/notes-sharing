from flask_jwt_extended import create_access_token
from app import mongo

class AuthService:

    def signup(username, password):
        if not username or not password:
            return {'message': 'Invalid Schema'}, 400
        if mongo.db.users.find_one({'username': username}):
            return {'message': 'Username already exists'}, 400
        mongo.db.users.insert_one({'username': username, 'password': password})
        return {'message': 'User created successfully'}, 201

    def login(username, password):
        user = mongo.db.users.find_one({'username': username, 'password': password})
        if user:
            access_token = create_access_token(identity=username)
            return {'username':username,'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401
