from flask import request, jsonify, Response
from app import app, limiter
from app.services.auth_service import AuthService
from flask_cors import cross_origin

@app.route('/api/auth/signup', methods=['POST'])
@limiter.limit('5 per minute')
@cross_origin()
def signup_route():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    response,code = AuthService.signup(username, password)
    return Response(status=code, response=jsonify(response).data, headers={'Content-Type': 'application/json'})

@app.route('/api/auth/login', methods=['POST'])
@cross_origin()
@limiter.limit('5 per minute')
def login_route():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    response,code = AuthService.login(username, password)
    return Response(status=code, response=jsonify(response).data, headers={'Content-Type': 'application/json'})
