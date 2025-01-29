from flask import Blueprint, request, jsonify
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

# Middleware: Kullanıcı doğrulama için bir decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            current_user = get_jwt_identity()
            if not current_user:
                return jsonify({"message": "Yetkisiz erişim. Token geçerli değil!"}), 401
        except Exception as e:
            return jsonify({"message": f"Token doğrulama hatası: {str(e)}"}), 401
        return f(*args, **kwargs)
    return decorated

# Blueprint tanımı
projects_bp = Blueprint('projects', __name__)

# Projeleri Listeleme (GET)
@projects_bp.route('/', methods=['GET'])
@jwt_required()
def get_projects():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM projects')
        projects = cursor.fetchall()

        result = [{'id': project[0], 'name': project[1], 'description': project[2], 'title': project[3]} for project in projects]
        cursor.close()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Yeni proje ekleme (POST)
@projects_bp.route('/', methods=['POST'])
@jwt_required()
def add_project():
    try:
        data = request.get_json()
        name = data.get('name')
        title = data.get('title')
        description = data.get('description')

        if not name or not title or not description:
            return jsonify({'message': 'name, title ve description alanları zorunludur!'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO projects (name, title, description) VALUES (%s, %s, %s)',
                       (name, title, description))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Proje başarıyla eklendi!'}), 201
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Proje güncelleme (PUT)
@projects_bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    try:
        data = request.get_json()
        name = data.get('name')
        title = data.get('title')
        description = data.get('description')

        if not name or not title or not description:
            return jsonify({'message': 'name, title ve description alanları zorunludur!'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE projects SET name = %s, title = %s, description = %s WHERE id = %s',
                       (name, title, description, project_id))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Proje başarıyla güncellendi!'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Proje silme (DELETE)
@projects_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
@token_required
def delete_project(project_id):
    try:
        # İlk olarak, projeye bağlı tüm görevleri sil
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM tasks WHERE project_id = %s', (project_id,))
        mysql.connection.commit()

        # Ardından projeyi sil
        cursor.execute('DELETE FROM projects WHERE id = %s', (project_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Proje ve bağlı görevler başarıyla silindi!'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
