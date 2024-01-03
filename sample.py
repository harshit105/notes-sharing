from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a secure, random key in production
jwt = JWTManager(app)

# In-memory user database (replace this with a proper database in a real application)
users = {
    'user1': {'password': 'password1'},
    'user2': {'password': 'password2'}
}

# In-memory notes database (replace this with a proper database in a real application)
notes = {
    'user1': [{'id': 1, 'content': 'Note 1'}, {'id': 2, 'content': 'Note 2'}],
    'user2': [{'id': 3, 'content': 'Note 3'}, {'id': 4, 'content': 'Note 4'}]
}

# Authentication Endpoints

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({'message': 'Username already exists'}), 400

    users[username] = {'password': password}
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username not in users or users[username]['password'] != password:
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# Note Endpoints

@app.route('/api/notes', methods=['GET'])
@jwt_required()
def get_notes():
    current_user = get_jwt_identity()
    return jsonify(notes.get(current_user, [])), 200

@app.route('/api/notes/<int:id>', methods=['GET'])
@jwt_required()
def get_note_by_id(id):
    current_user = get_jwt_identity()
    user_notes = notes.get(current_user, [])
    note = next((n for n in user_notes if n['id'] == id), None)
    if note:
        return jsonify(note), 200
    else:
        return jsonify({'message': 'Note not found'}), 404

@app.route('/api/notes', methods=['POST'])
@jwt_required()
def create_note():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_note = {'id': len(notes.get(current_user, [])) + 1, 'content': data.get('content')}
    notes.setdefault(current_user, []).append(new_note)
    return jsonify(new_note), 201

@app.route('/api/notes/<int:id>', methods=['PUT'])
@jwt_required()
def update_note_by_id(id):
    current_user = get_jwt_identity()
    user_notes = notes.get(current_user, [])
    note = next((n for n in user_notes if n['id'] == id), None)
    if note:
        data = request.get_json()
        note['content'] = data.get('content')
        return jsonify(note), 200
    else:
        return jsonify({'message': 'Note not found'}), 404

@app.route('/api/notes/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_note_by_id(id):
    current_user = get_jwt_identity()
    user_notes = notes.get(current_user, [])
    note_index = next((index for index, n in enumerate(user_notes) if n['id'] == id), None)
    if note_index is not None:
        deleted_note = user_notes.pop(note_index)
        return jsonify(deleted_note), 200
    else:
        return jsonify({'message': 'Note not found'}), 404

@app.route('/api/notes/<int:id>/share', methods=['POST'])
@jwt_required()
def share_note_with_user(id):
    current_user = get_jwt_identity()
    data = request.get_json()
    share_with_user = data.get('username')

    if share_with_user not in users:
        return jsonify({'message': 'User not found'}), 404

    user_notes = notes.get(current_user, [])
    note = next((n for n in user_notes if n['id'] == id), None)
    if note:
        # Implement your logic for sharing the note with the specified user
        return jsonify({'message': 'Note shared successfully'}), 200
    else:
        return jsonify({'message': 'Note not found'}), 404

@app.route('/api/search', methods=['GET'])
@jwt_required()
def search_notes():
    current_user = get_jwt_identity()
    query = request.args.get('q', '')

    # Implement your logic for searching notes based on keywords
    # This is just a placeholder response
    return jsonify({'message': f'Searching notes for query: {query}'}), 200

if __name__ == '__main__':
    app.run(debug=True)
