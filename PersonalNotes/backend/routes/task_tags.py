from flask import Blueprint, request, jsonify
from extensions import mysql
from flask_jwt_extended import jwt_required

# Blueprint oluşturuyoruz
task_tags_bp = Blueprint('task_tags', __name__)

# Yeni task-tag ekleme (POST)
@task_tags_bp.route('/', methods=['POST'])
@jwt_required()  # JWT doğrulaması
def add_task_tag():
    try:
        # JSON verisini alıyoruz
        data = request.get_json()
        task_id = data.get('task_id')
        tag_id = data.get('tag_id')

        # Parametre kontrolü
        if not task_id or not tag_id:
            return jsonify({"msg": "Task ID and Tag ID are required!"}), 400

        # Veritabanına task-tag ilişkisini ekliyoruz
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO task_tags (task_id, tag_id) VALUES (%s, %s)', (task_id, tag_id))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"msg": "Task-Tag successfully added!"}), 201

    except Exception as e:
        return jsonify({"msg": f"Error: {str(e)}"}), 500


# Task-Tag ilişkisini alma (GET)
@task_tags_bp.route('/', methods=['GET'])
@jwt_required()  # JWT doğrulaması
def get_task_tags():
    try:
        # Veritabanından task-tag ilişkilerini alıyoruz
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM task_tags')
        task_tags = cursor.fetchall()
        cursor.close()

        # Task-Tag ilişkilerini formatlayarak JSON formatında döndürüyoruz
        result = [{'task_id': task_tag[0], 'tag_id': task_tag[1]} for task_tag in task_tags]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"msg": f"Error: {str(e)}"}), 500


# Task-Tag ilişkisini güncelleme (PUT)
@task_tags_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()  # JWT doğrulaması
def update_task_tag(id):
    try:
        # JSON verisini alıyoruz
        data = request.get_json()
        task_id = data.get('task_id')
        tag_id = data.get('tag_id')

        # Parametre kontrolü
        if not task_id or not tag_id:
            return jsonify({"msg": "Task ID and Tag ID are required!"}), 400

        # Veritabanında task-tag ilişkisini güncelliyoruz
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE task_tags SET task_id = %s, tag_id = %s WHERE id = %s', (task_id, tag_id, id))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"msg": "Task-Tag successfully updated!"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error: {str(e)}"}), 500


# Task-Tag ilişkisini silme (DELETE)
@task_tags_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()  # JWT doğrulaması
def delete_task_tag(id):
    try:
        # Veritabanından task-tag ilişkisini siliyoruz
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM task_tags WHERE id = %s', (id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"msg": "Task-Tag successfully deleted!"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error: {str(e)}"}), 500
