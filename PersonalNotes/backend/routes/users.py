from flask import Blueprint, request, jsonify
from extensions import mysql
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from functools import wraps

users_bp = Blueprint('users', __name__)


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

from flask import Blueprint, request, jsonify
from extensions import mysql
from flask_jwt_extended import create_access_token

# Blueprint tanımı
users_bp = Blueprint('users', __name__, url_prefix='/users')

# Kullanıcı kaydı (POST)
@users_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username ve password alanları zorunludur!'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Users (username, password) VALUES (%s, %s)', (username, password))
        mysql.connection.commit()
        cursor.close()

        # Kullanıcı kaydından sonra token oluştur
        access_token = create_access_token(identity=str(username))
        return jsonify({'message': 'Kullanıcı başarıyla eklendi!', 'access_token': access_token}), 201
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500



@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, username, role FROM Users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    user_id, username, role = user

    # Token oluştururken identity alanını bir string olarak gönderin
    token = create_access_token(identity=str(user_id))  # ID'yi string formatına çevirin
    return jsonify({'access_token': token}), 200



# Tüm kullanıcıları listeleme (GET)
@users_bp.route('/', methods=['GET'])
@jwt_required()  # Token zorunluluğu
def get_users():
    try:
        current_user = get_jwt_identity()  # Mevcut kullanıcıyı al

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id, username,role FROM Users')  # Şifreyi çekmemek daha güvenli
        users = cursor.fetchall()

        result = [{'id': user[0], 'username': user[1], 'role':user[2]} for user in users]
        cursor.close()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Yeni kullanıcı ekleme (POST)
@users_bp.route('/add', methods=['POST'])
@users_bp.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username ve password alanları zorunludur!'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Users (username, password) VALUES (%s, %s)', (username, password))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Kullanıcı başarıyla eklendi!'}), 201
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Kullanıcı güncelleme (PUT)
@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()  # Token koruması
@token_required
def update_user(user_id):
    try:
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
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Kullanıcı silme (DELETE)
@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@token_required
def delete_user(user_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Users WHERE id = %s', (user_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Kullanıcı başarıyla silindi!'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

