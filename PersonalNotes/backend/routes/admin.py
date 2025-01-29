from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mysql
from utils import admin_required  # admin_required decorator'ını import et


admin_bp = Blueprint('admin', __name__)

# Admin paneline sadece admin erişebilir
@admin_bp.route('/panel', methods=['GET'])
@jwt_required()  # Token zorunluluğu
def admin_panel():
    try:
        current_user = get_jwt_identity()  # JWT token'dan kullanıcı kimliği alınır
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT role FROM Users WHERE id = %s', (current_user,))
        user = cursor.fetchone()
        cursor.close()

        if user and user[0] == 'admin':  # Admin kontrolü
            return jsonify(msg="Welcome to the admin panel!")
        else:
            return jsonify(msg="Erişim reddedildi! Admin yetkisi gereklidir."), 403
    except Exception as e:
        return jsonify(msg=f"Error: {str(e)}"), 500

# Admin'in tüm kullanıcıları listeleme (GET)
@admin_bp.route('/users', methods=['GET'])
@admin_bp.route('/admin', methods=['GET'])
@jwt_required()  # Token zorunluluğu
def get_all_users():
    try:
        current_user = get_jwt_identity()  # JWT token'dan kullanıcı kimliği alınır
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT role FROM Users WHERE id = %s', (current_user,))
        user = cursor.fetchone()
        cursor.close()

        # Admin kontrolü
        if user and user[0] == 'admin':  # Kullanıcı admin mi?
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT id, username,role FROM Users')
            users = cursor.fetchall()
            cursor.close()

            result = [{'id': user[0], 'username': user[1],'role':user[2]} for user in users]
            return jsonify(result), 200
        else:
            return jsonify({"msg": "Erişim reddedildi! Admin yetkisi gereklidir."}), 403

    except Exception as e:
        return jsonify({"msg": f"Error: {str(e)}"}), 500

# Admin kullanıcı ekleme (POST)
@admin_bp.route('/users', methods=['POST'])
@admin_bp.route('/admin', methods=['POST'])
@jwt_required()  # Token zorunluluğu
def add_user_by_admin():
    try:
        current_user = get_jwt_identity()

        # Kullanıcının admin olup olmadığını kontrol et
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT role FROM Users WHERE id = %s', (current_user,))
        user = cursor.fetchone()
        cursor.close()

        if user and user[0] == 'admin':  # Admin kontrolü
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            role = data.get('role', 'user')  # Varsayılan olarak user rolü ekle

            if not username or not password:
                return jsonify({'message': 'Username ve password alanları zorunludur!'}), 400

            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)', (username, password, role))
            mysql.connection.commit()
            cursor.close()

            return jsonify({'message': 'Kullanıcı başarıyla eklendi!'}), 201
        else:
            return jsonify({"msg": "Erişim reddedildi! Admin yetkisi gereklidir."}), 403
    except Exception as e:
        return jsonify({"msg": f"Error: {str(e)}"}), 500

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@admin_bp.route('/admin/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_by_admin(user_id):
    current_user = get_jwt_identity()  # JWT token'dan kullanıcı kimliği alınır

    # Admin olup olmadığını kontrol et
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT role FROM Users WHERE id = %s', (current_user,))
    user = cursor.fetchone()  # Kullanıcının rolünü al
    cursor.close()

    if user and user[0] == 'admin':  # Eğer kullanıcı adminse
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username ve password alanları zorunludur!'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE Users SET username = %s, password = %s WHERE id = %s',
                       (username, password, user_id))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Kullanıcı başarıyla güncellendi!'}), 200
    else:
        return jsonify({"msg": "Erişim reddedildi! Admin yetkisi gereklidir."}), 403

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user_by_admin(user_id):
    try:
        current_user = get_jwt_identity()  # JWT token'dan kullanıcı kimliği alınır

        # Admin olup olmadığını kontrol et
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT role FROM Users WHERE id = %s', (current_user,))
        user = cursor.fetchone()  # Kullanıcının rolünü al

        if not user or user[0] != 'admin':  # Eğer kullanıcı admin değilse
            cursor.close()
            return jsonify({"msg": "Erişim reddedildi! Admin yetkisi gereklidir."}), 403

        # Kullanıcı silme işlemi
        cursor.execute('DELETE FROM Users WHERE id = %s', (user_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Kullanıcı başarıyla silindi!'}), 200
    except Exception as e:
        return jsonify({"msg": f"Hata oluştu: {str(e)}"}), 500

# Admin istatistikleri (GET)
@admin_bp.route('/stats', methods=['GET'])
@jwt_required()  # Token zorunluluğu
def admin_stats():
    try:
        current_user = get_jwt_identity()
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT role FROM Users WHERE id = %s', (current_user,))
        user = cursor.fetchone()
        cursor.close()

        if user and user[0] == 'admin':  # Admin kontrolü
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM Users')
            total_users = cursor.fetchone()[0]
            cursor.close()

            return jsonify({'total_users': total_users}), 200
        else:
            return jsonify({"msg": "Erişim reddedildi! Admin yetkisi gereklidir."}), 403
    except Exception as e:
        return jsonify({"msg": f"Error: {str(e)}"}), 500



@admin_bp.route('/check-admin', methods=['GET'])
@jwt_required()
def check_admin():
    try:
        user_id = get_jwt_identity()  # Token'dan identity alınır
        print(f"User ID from token: {user_id}")

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT role FROM Users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if not user:
            return jsonify({'is_admin': False}), 200

        role = user[0]
        return jsonify({'is_admin': role == 'admin'}), 200
    except Exception as e:
        return jsonify({'message': f'Hata oluştu: {str(e)}'}), 500

@admin_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    try:
        current_user = get_jwt_identity()  # Kullanıcı bilgisi
        cursor = mysql.connection.cursor()

        # Kullanıcının rolünü kontrol et
        cursor.execute("SELECT role FROM Users WHERE id = %s", (current_user,))
        user_role = cursor.fetchone()

        if user_role and user_role[0] == 'admin':
            # Admin ise tüm görevleri al
            cursor.execute("""
                SELECT 
                    Tasks.id, 
                    Tasks.title, 
                    Tasks.description, 
                    Tasks.user_id, 
                    Projects.name AS project_name, 
                    Tags.name AS tag_name,
                    Users.username AS assigned_by
                FROM Tasks
                LEFT JOIN Projects ON Tasks.project_id = Projects.id
                LEFT JOIN Tags ON Tasks.tags_id = Tags.id
                LEFT JOIN Users ON Tasks.user_id = Users.id
            """)
        else:
            # Normal kullanıcı ise yalnızca kendi görevlerini al
            cursor.execute("""
                SELECT 
                    Tasks.id, 
                    Tasks.title, 
                    Tasks.description, 
                    Tasks.user_id, 
                    Projects.name AS project_name, 
                    Tags.name AS tag_name,
                    Users.username AS assigned_by
                FROM Tasks
                LEFT JOIN Projects ON Tasks.project_id = Projects.id
                LEFT JOIN Tags ON Tasks.tags_id = Tags.id
                LEFT JOIN Users ON Tasks.user_id = Users.id
                WHERE Tasks.user_id = %s
            """, (current_user,))

        tasks = cursor.fetchall()
        cursor.close()

        # JSON formatına dönüştür
        result = [
            {
                'id': task[0],
                'title': task[1],
                'description': task[2],
                'user_id': task[3],
                'project_name': task[4],
                'tag_name': task[5],
                'assigned_by': task[6]
            }
            for task in tasks
        ]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@admin_bp.route('/projects', methods=['GET'])
@jwt_required()
def get_projects():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, name, description, title FROM Projects")
        projects = cursor.fetchall()
        cursor.close()

        result = [
            {'id': project[0], 'name': project[1], 'description': project[2], 'title': project[3]}
            for project in projects
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
@admin_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM Projects WHERE id = %s", (project_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Project deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
@admin_bp.route('/projects', methods=['POST'])
@jwt_required()
def add_project():
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        title = data.get('title')

        if not name or not description or not title:
            return jsonify({'message': 'All fields are required!'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO Projects (name, description, title) VALUES (%s, %s, %s)",
            (name, description, title)
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Project added successfully!'}), 201
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
@admin_bp.route('/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note_by_admin(note_id):
    try:
        user_id = get_jwt_identity()
        cursor = mysql.connection.cursor()

        # Kullanıcının rolünü kontrol et
        cursor.execute("SELECT role FROM Users WHERE id = %s", (user_id,))
        user_role = cursor.fetchone()

        if not user_role or user_role[0] != 'admin':
            return jsonify({'message': 'Unauthorized: Only admins can delete notes'}), 403

        # Notun var olup olmadığını kontrol et
        cursor.execute("SELECT id FROM Notes WHERE id = %s", (note_id,))
        note_exists = cursor.fetchone()

        if not note_exists:
            return jsonify({'message': 'Note not found'}), 404

        # Notu sil
        cursor.execute("DELETE FROM Notes WHERE id = %s", (note_id,))
        mysql.connection.commit()

        return jsonify({'message': 'Note deleted successfully by admin!'}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

    finally:
        cursor.close()
@admin_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task_by_admin(task_id):
    try:
        # Admin yetkisini kontrol et
        current_user = get_jwt_identity()
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT role FROM Users WHERE id = %s", (current_user,))
        role = cursor.fetchone()

        if not role or role[0] != 'admin':
            return jsonify({'message': 'Unauthorized access! Admin role required.'}), 403

        # Görevi sil
        cursor.execute("DELETE FROM Tasks WHERE id = %s", (task_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Task deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
