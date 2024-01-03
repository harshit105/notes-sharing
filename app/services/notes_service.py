from app import mongo
from flask import Response, jsonify
from ..custom_converters import CustomJSONEncoder
from bson import ObjectId

class NotesService:

    def get_notes(current_user):
        try:
            user_notes = list(mongo.db.notes.find({'username': current_user}))
            for note in user_notes:
                note['_id'] = str(note['_id'])
            response=jsonify({'notes': user_notes}).data
            status=200
            return response,status
        except Exception as e:
            response = jsonify({'msg': 'Internal Server Error'}).data
            return response, 500


    def get_note_by_id(current_user, note_id):
        note_id_obj = ObjectId(note_id)
        try:
            note = mongo.db.notes.find_one({'_id': note_id_obj, 'username': current_user})
            if note:
                note['_id'] = str(note['_id'])
                response = jsonify({'notes': note}).data
                return response, 200
            else:
                response = jsonify({'msg': 'Note not found'}).data
                return response, 404
        except Exception as e:
            response = jsonify({'msg': 'Internal Server Error'}).data
            return response, 500


    def create_note(current_user, note_data):
        try:
            if not note_data.get('content'):
                response=jsonify({'message': 'Can\'t create empty note'}).data
                return response,500
            else:
                new_note = {'username': current_user, 'content': note_data.get('content')}
                mongo.db.notes.insert_one(new_note)
                response=jsonify({'message': 'Note created successfully'}).data
                return response,200
        except Exception as e:
            response = jsonify({'msg': 'Internal Server Error'}).data
            return response, 500


    def update_note(current_user, note_id, updated_data):
        try:
            if not updated_data.get('content'):
                response=jsonify({'message': 'Can\'t update to empty note'}).data
                return response,500
            else:
                mongo.db.notes.update_one({'_id': note_id, 'username': current_user}, {'$set': updated_data})
                response=jsonify({'message': 'Note updated successfully'}).data
                status=200
                return response,status
        except Exception as e:
            response = jsonify({'msg': 'Internal Server Error'}).data
            return response, 500


    def delete_note(current_user, note_id):
        try:
            mongo.db.notes.delete_one({'_id': note_id, 'username': current_user})
            response=jsonify({'message': 'Note deleted successfully'}).data
            status=200
            return response,status
        except Exception as e:
            response = jsonify({'msg': 'Internal Server Error'}).data
            return response, 500
