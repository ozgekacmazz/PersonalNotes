from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify
from extensions import mysql


# Middleware: Kullanıcı doğrulama için bir decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            current_user = get_jwt_identity()  # Kullanıcının kimliğini al
            if not current_user:  # Eğer kullanıcı kimliği yoksa
                return jsonify({"message": "Yetkisiz erişim. Token geçerli değil!"}), 401
        except Exception as e:
            return jsonify({"message": f"Token doğrulama hatası: {str(e)}"}), 401
        return f(*args, **kwargs)

    return decorated


# Admin rolü kontrol fonksiyonu
def is_admin():
    current_user = get_jwt_identity()

    # Veritabanı sorgusu ile admin kontrolü yapılabilir
    # Örnek olarak burada basit bir kontrol gösterilmektedir
    # Veritabanından kullanıcıyı kontrol etmek için:
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT role FROM Users WHERE id = %s', (current_user,))
    user = cursor.fetchone()
    cursor.close()

    if user and user[0] == 'admin':
        return True
    return False


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user is None or current_user['role'] != 'admin':
            return jsonify({"msg": "Erişim reddedildi! Admin yetkisi gereklidir."}), 403
        return f(*args, **kwargs)
    return decorated_function
