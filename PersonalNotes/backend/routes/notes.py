from flask import Blueprint, request, jsonify
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity

# Blueprint tanımı
notes_bp = Blueprint('notes', __name__)

# Tüm notları listeleme (GET)
@notes_bp.route('/', methods=['GET'])
@jwt_required()
def get_notes():
    try:
        user_id = get_jwt_identity()  # JWT'den kullanıcı kimliğini al
        cursor = mysql.connection.cursor()

        # Notes ve Users tablolarını birleştirerek notları kullanıcı adıyla birlikte al
        cursor.execute("""
            SELECT Notes.id, Notes.title, Notes.content, Notes.user_id, Users.username
            FROM Notes
            JOIN Users ON Notes.user_id = Users.id
        """)
        notes = cursor.fetchall()
        cursor.close()

        # JSON formatına dönüştür
        result = [
            {
                'id': note[0],
                'title': note[1],
                'content': note[2],
                'user_id': note[3],
                'username': note[4]  # Kullanıcı adı (Users tablosundan)
            }
            for note in notes
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@notes_bp.route('/', methods=['POST'])
@jwt_required()
def add_note():
    try:
        user_id = get_jwt_identity()  # JWT'den kullanıcı kimliğini al
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            return jsonify({'message': 'Title and content are required!'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO Notes (title, content, user_id) VALUES (%s, %s, %s)",
            (title, content, user_id)
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Note added successfully!'}), 201
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
@notes_bp.route('/<int:note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    try:
        user_id = get_jwt_identity()  # JWT'den kullanıcı kimliğini al
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            return jsonify({'message': 'Title and content are required!'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE Notes SET title = %s, content = %s WHERE id = %s AND user_id = %s",
            (title, content, note_id, user_id)
        )
        if cursor.rowcount == 0:
            return jsonify({'message': 'Note not found or not authorized to update!'}), 403

        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Note updated successfully!'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
@notes_bp.route('/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    try:
        user_id = get_jwt_identity()  # JWT'den kullanıcı kimliğini al

        cursor = mysql.connection.cursor()
        cursor.execute(
            "DELETE FROM Notes WHERE id = %s AND user_id = %s",
            (note_id, user_id)
        )
        if cursor.rowcount == 0:
            return jsonify({'message': 'Note not found or not authorized to delete!'}), 403

        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Note deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
