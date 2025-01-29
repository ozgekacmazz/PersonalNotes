# tasks.py

from flask import Blueprint, request, jsonify
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity

tasks_bp = Blueprint('tasks', __name__)

# Tüm görevleri listeleme (GET)
@tasks_bp.route('/', methods=['GET'])
@jwt_required()  # Token zorunluluğu
def get_tasks():
    try:
        current_user = get_jwt_identity()  # Kullanıcı bilgisi
        cursor = mysql.connection.cursor()

        # Görevleri proje adı ve etiket adı ile birlikte al
        cursor.execute("""
            SELECT 
                Tasks.id, 
                Tasks.title, 
                Tasks.description, 
                Tasks.user_id, 
                Projects.name AS project_name, 
                Tags.name AS tag_name
            FROM Tasks
            LEFT JOIN Projects ON Tasks.project_id = Projects.id
            LEFT JOIN Tags ON Tasks.tags_id = Tags.id
            WHERE Tasks.user_id = %s
        """, (current_user,))
        tasks = cursor.fetchall()

        # JSON formatına dönüştür
        result = [
            {
                'id': task[0],
                'title': task[1],
                'description': task[2],
                'user_id': task[3],
                'project_name': task[4],  # Proje adı
                'tag_name': task[5]       # Etiket adı
            }
            for task in tasks
        ]
        cursor.close()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


# Belirli bir görevi getirme (GET)
@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()  # Token zorunluluğu
def get_task(task_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Tasks WHERE id = %s', (task_id,))
        task = cursor.fetchone()

        if not task:
            return jsonify({'message': 'Görev bulunamadı!'}), 404

        result = {'id': task[0], 'title': task[1], 'description': task[2], 'user_id': task[3], 'project_id': task[4]}
        cursor.close()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def add_task():
    data = request.get_json()
    user_id = get_jwt_identity()  # Token'dan user_id al
    title = data.get('title')
    description = data.get('description')
    project_id = data.get('project_id')
    tags_id = data.get('tags_id')  # Bu, bir liste olabilir.

    if not title or not description or not project_id:
        return jsonify({'message': 'Title, description, and project_id are required'}), 400

    # Eğer tags_id bir listeyse string olarak saklayın (örnek: "1,2,3")
    if isinstance(tags_id, list):
        tags_id = ",".join(map(str, tags_id))

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO Tasks (user_id, project_id, title, description, tags_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, project_id, title, description, tags_id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Task added successfully'}), 201

# Görev güncelleme (PUT)
@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()  # Token zorunluluğu
def update_task(task_id):
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        project_id = data.get('project_id')

        if not title or not description or not project_id:
            return jsonify({'message': 'title, description ve project_id alanları zorunludur!'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE Tasks SET title = %s, description = %s, project_id = %s WHERE id = %s',
                       (title, description, project_id, task_id))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Görev başarıyla güncellendi!'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Görev silme (DELETE)
@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()  # Token zorunluluğu
def delete_task(task_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Tasks WHERE id = %s', (task_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Görev başarıyla silindi!'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
