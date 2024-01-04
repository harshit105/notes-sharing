from app import mongo
from flask import Response, jsonify
from ..custom_converters import CustomJSONEncoder
from bson import ObjectId

class NotesService:
    def get_notes(current_user):
        try:
            user_notes = list(mongo.db.notes.find({'username': current_user}))
            shared_notes = list(mongo.db.notes.find({'shared_with': current_user}))
            all_notes = user_notes+shared_notes
            for note in all_notes:
                note['_id'] = str(note['_id'])
            return jsonify({'notes': all_notes}).data,200
        except Exception as e:
            print(e)
            response = jsonify({'msg': 'Internal Server Error'}).data
            return response, 500


    def get_note_by_id(current_user, note_id):
        note_id_obj = ObjectId(note_id)
        try:
            note = mongo.db.notes.find_one({'_id': note_id_obj, 'username': current_user}) or mongo.db.notes.find_one({'_id':note_id_obj,'shared_with':current_user})
            if note:
                note['_id'] = str(note['_id'])
                return jsonify({'notes': note}).data, 200
            else:
                return jsonify({'message': 'Note not found or does not belong to the user'}).data, 404
        except Exception as e:
            print(e)
            response = jsonify({'msg': 'Internal Server Error'}).data
            return response, 500


    def create_note(current_user, note_data):
        try:
            if not note_data.get('content'):
                response=jsonify({'message': 'Can\'t create empty note'}).data
                return response,500
            else:
                new_note = {
                    'username': current_user,
                    'content': note_data.get('content'),
                    'shared_with': []
                }
                result = mongo.db.notes.insert_one(new_note)
                response=jsonify({'message': 'Note created successfully', 'note_id':str(result.inserted_id)}).data
                return response,200
        except Exception as e:
            print(e)
            return jsonify({'msg': 'Internal Server Error'}).data, 500


    def update_note(current_user, note_id, updated_data):
        try:
            if not updated_data.get('content'):
                response=jsonify({'message': 'Can\'t update to empty note'}).data
                return response,500
            else:
                updated_note = {
                    'content': updated_data.get('content')
                }
                result = mongo.db.notes.update_one({'_id': note_id, 'username': current_user}, {'$set': updated_note})
                if result.modified_count > 0:
                    return jsonify({'message': 'Note updated successfully'}).data, 200
                else:
                    return jsonify({'message': 'Note not found or does not belong to the user or no updates'}).data, 404
        except Exception as e:
            print(e)
            return jsonify({'msg': 'Internal Server Error'}).data, 500


    def delete_note(current_user, note_id):
        try:
            result = mongo.db.notes.delete_one({'_id': note_id, 'username': current_user})
            if result.deleted_count > 0:
                return jsonify({'message': 'Note deleted successfully'}).data, 200
            else:
                return jsonify({'message': 'Note not found or does not belong to the user'}).data, 404
        except Exception as e:
            print(e)
            return jsonify({'msg': 'Internal Server Error'}).data, 500


    def share_note(current_user, target_user, note_id):
        try:
            # Validate that the target user is provided in the request
            if not target_user:
                return jsonify({'message': 'Target user not provided'}).data, 400

            if target_user == current_user:
                return jsonify({'message': "Can't share with yourself"}).data, 400

            # Check if the note exists and belongs to the authenticated user
            note = mongo.db.notes.find_one({'_id': note_id, 'username': current_user})
            if not note:
                return jsonify({'message': 'Note not found or does not belong to the user'}).data, 404

            # Check if the target user exists
            target_user_doc = mongo.db.users.find_one({'username': target_user})
            if not target_user_doc:
                return jsonify({'message': 'Target user not found'}).data, 404

            # Check if the note is already shared with the target user
            if target_user in note.get('shared_with', []):
                return jsonify({'message': f'Note is already shared with {target_user}'}).data, 200

            # Update the note's 'shared_with' field
            mongo.db.notes.update_one(
                {'_id': ObjectId(note_id), 'username':current_user},
                {'$push': {'shared_with': target_user}}
            )
            return jsonify({'message': f'Note shared with {target_user}'}).data, 200

        except Exception as e:
            print(e)
            return jsonify({'message': 'Internal Server Error'}).data, 500


    def search_notes(current_user, query):
        try:
            mongo.db.notes.create_index([('content', 'text')])
            cursor = mongo.db.notes.find(
                {
                    '$and': [
                        {'$or': [{'username': current_user}, {'shared_with': current_user}]},
                        {'$text': {'$search': query}}
                    ]
                },
                {'score': {'$meta': 'textScore'}}
            ).sort([('score', {'$meta': 'textScore'})])
            search_results = [{'_id': str(note['_id']), 'score': note['score'],'content':note['content'],'username':note['username']} for note in cursor]
            return jsonify({'search_result':search_results}).data,200
        except ArithmeticError as e:
            print(e)
            return jsonify({'message': 'Internal Server Error'}).data, 500
