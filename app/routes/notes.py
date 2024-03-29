from flask import request, jsonify, Response
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import app, limiter
from app.services.notes_service import NotesService
from flask_cors import cross_origin

@app.route('/api/notes', methods=['GET'])
@jwt_required()
@cross_origin()
@limiter.limit('100 per minute')
def get_notes_route():
    current_user = get_jwt_identity()
    response, status = NotesService.get_notes(current_user)
    response = Response(response=response,status=status,headers={'Content-Type': 'application/json'})
    return response

@app.route('/api/notes/<ObjectId:note_id>', methods=['GET'])
@jwt_required()
@cross_origin()
@limiter.limit('100 per minute')
def get_note_by_id_route(note_id):
    current_user = get_jwt_identity()
    response,status =  NotesService.get_note_by_id(current_user, note_id)
    response = Response(response=response,status=status,headers={'Content-Type': 'application/json'})
    return response

@app.route('/api/notes', methods=['POST'])
@jwt_required()
@cross_origin()
@limiter.limit('10 per minute')
def create_note_route():
    current_user = get_jwt_identity()
    note_data = request.get_json()
    response,status =  NotesService.create_note(current_user, note_data)
    response = Response(response=response,status=status,headers={'Content-Type': 'application/json'})
    return response

@app.route('/api/notes/<ObjectId:note_id>', methods=['PUT'])
@jwt_required()
@cross_origin()
@limiter.limit('10 per minute')
def update_note_route(note_id):
    current_user = get_jwt_identity()
    updated_data = request.get_json()
    response,status =  NotesService.update_note(current_user, note_id, updated_data)
    response = Response(response=response,status=status,headers={'Content-Type': 'application/json'})
    return response

@app.route('/api/notes/<ObjectId:note_id>', methods=['DELETE'])
@jwt_required()
@cross_origin()
@limiter.limit('50 per minute')
def delete_note_route(note_id):
    current_user = get_jwt_identity()
    response, status =  NotesService.delete_note(current_user, note_id)
    response = Response(response=response,status=status,headers={'Content-Type': 'application/json'})
    return response

@app.route('/api/notes/<ObjectId:note_id>/share', methods=['POST'])
@jwt_required()
@cross_origin()
@limiter.limit('10 per minute')
def share_note_with_user(note_id):
    current_user = get_jwt_identity()
    target_user = request.json.get('target_user')
    response, status =  NotesService.share_note(current_user,target_user,note_id)
    response = Response(response=response,status=status,headers={'Content-Type': 'application/json'})
    return response
