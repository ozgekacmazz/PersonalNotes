from flask import Blueprint, request, jsonify
from extensions import mysql
from flask_jwt_extended import jwt_required
from flask import current_app

# Blueprint oluşturuyoruz
tags_bp = Blueprint('tags', __name__)

# Yeni etiket ekleme (POST)
@tags_bp.route('/', methods=['POST'])
@tags_bp.route('/admin/tags', methods=['POST'])
@jwt_required()  # JWT doğrulaması
def add_tag():
    try:
        # JSON verisini alıyoruz
        data = request.get_json()
        print(data)
        name = data.get('name')

        current_app.logger.debug(f"Received 'name' parameter: {name} - Type: {type(name)}")

        # Log yazdırma - name parametresini kontrol et
        print(f"Received name: {name}")  # Bu logu görmek için terminali kontrol edin.

        # name alanı kontrolü
        if not name:
            return jsonify({"msg": "Name is required!"}), 400
        if not isinstance(name, str):
            return jsonify({"msg": "Name must be a string!"}), 400

        # Veritabanına etiket ekleme
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Tags (name) VALUES (%s)', (name,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"msg": "Tag successfully added!"}), 201

    except Exception as e:
        return jsonify({"msg": f"Error: {str(e)}"}), 500


# Etiketleri listeleme (GET)
@tags_bp.route('/', methods=['GET'])
@tags_bp.route('/admin/tags', methods=['GET'])
@jwt_required()  # JWT doğrulaması
def get_tags():
    try:
        # Veritabanından etiketleri alıyoruz
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Tags')
        tags = cursor.fetchall()
        cursor.close()

        # Etiketleri formatlayarak JSON formatında döndürüyoruz
        result = [{'id': tag[0], 'name': tag[1]} for tag in tags]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"msg": f"Error: {str(e)}"}), 500


# Etiket güncelleme (PUT)
@tags_bp.route('/<int:tag_id>', methods=['PUT'])
@tags_bp.route('/admin/tags/<int:tag_id>', methods=['PUT'])
@jwt_required()  # JWT doğrulaması
def update_tag(tag_id):
    try:
        # JSON verisini alıyoruz
        data = request.get_json()
        name = data.get('name')

        # name alanı kontrolü
        if not name:
            return jsonify({"msg": "Name is required!"}), 400
        if not isinstance(name, str):
            return jsonify({"msg": "Name must be a string!"}), 400

        # Veritabanında etiketi güncelliyoruz
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE Tags SET name = %s WHERE id = %s', (name, tag_id))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"msg": "Tag successfully updated!"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error: {str(e)}"}), 500


# Etiket silme (DELETE)
@tags_bp.route('/<int:tag_id>', methods=['DELETE'])
@tags_bp.route('/admin/tags/<int:tag_id>', methods=['DELETE'])

@jwt_required()  # JWT doğrulaması
def delete_tag(tag_id):
    try:
        # Veritabanından etiketi siliyoruz
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Tags WHERE id = %s', (tag_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"msg": "Tag successfully deleted!"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error: {str(e)}"}), 500
