from flask import request, jsonify, Response
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import app, limiter
from app.services.notes_service import NotesService
from flask_cors import cross_origin

@app.route('/api/search', methods=['GET'])
@jwt_required()
@cross_origin()
@limiter.limit('10 per minute')
def search_notes():
    current_user = get_jwt_identity()
    query = request.args.get('q', '')
    response, status = NotesService.search_notes(current_user, query)
    response = Response(response=response,status=status,headers={'Content-Type': 'application/json'})
    return response
