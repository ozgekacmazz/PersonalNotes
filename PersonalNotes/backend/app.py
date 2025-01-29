import logging
from flask import Flask, jsonify
from config import Config
from extensions import mysql, jwt
from routes.users import users_bp
from routes.notes import notes_bp
from routes.tasks import tasks_bp
from routes.projects import projects_bp
from routes.tags import tags_bp
from routes.task_tags import task_tags_bp
from flask_cors import CORS
from routes.admin import admin_bp
from flask_jwt_extended import jwt_required, JWTManager





def create_app():
    app = Flask(__name__)
    CORS(app)  # CORS ayarlarını aktif ediyoruz
    jwt = JWTManager(app)
    app.config.from_object(Config)

    # Burada JWT SECRET KEY'ini ayarlıyoruz
    app.config['JWT_SECRET_KEY'] = 'gizli_anahtar'

    @app.route('/protected-route', methods=['GET'])
    @jwt_required()  # JWT gereksinimi
    def protected_route():
        return jsonify(message="Bu route'a yalnızca yetkili kullanıcılar erişebilir!")

    import logging

    # Loglama yapılandırması
    logging.basicConfig(level=logging.DEBUG,  # Log seviyesi DEBUG
                        format='%(asctime)s - %(levelname)s - %(message)s',  # Log formatı
                        handlers=[
                            logging.StreamHandler(),  # Logları terminale yazdır
                            logging.FileHandler('app_logs.log', encoding='utf-8')  # Logları dosyaya UTF-8 ile kaydet
                        ])

    app.logger.debug('Debug log mesajı')  # Debug log mesajı
    app.logger.info('Info log mesajı')   # Info log mesajı
    app.logger.warning('Warning log mesajı')  # Uyarı log mesajı
    app.logger.error('Error log mesajı')  # Hata log mesajı

    # Konfigürasyon ayarlarını yükle
    app.config.from_object(Config)

    # Uzantıları başlat
    mysql.init_app(app)  # MySQL bağlantısını başlat
    jwt.init_app(app)  # JWTManager'ı başlat ve Flask'e bağla

    # Blueprint'leri uygulamaya kaydet
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(notes_bp, url_prefix='/notes')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(projects_bp, url_prefix='/projects')
    app.register_blueprint(tags_bp, url_prefix='/tags')
    app.register_blueprint(task_tags_bp, url_prefix='/task-tags')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Ana sayfa route'u
    @app.route('/')
    def home():
        return "Kişisel Notlar API'sine hoş geldiniz!"



    @app.route('/log_test', methods=['GET'])
    def log_test():
        app.logger.debug("Bu bir debug mesajıdır!")
        app.logger.info("Bu bir info mesajıdır!")
        app.logger.warning("Bu bir uyarı mesajıdır!")
        app.logger.error("Bu bir hata mesajıdır!")
        app.logger.critical("Bu bir kritik mesajdır!")
        return "Loglar başarıyla yazıldı!"
        # Veritabanı bağlantısını kontrol et (ilk istekten önce)


    def test_db_connection():
        try:
            # Veritabanı bağlantısını uygulama bağlamında kontrol et
            with app.app_context():  # Uygulama bağlamı içinde çalıştırma
                connection = mysql.connection
                cursor = connection.cursor()
                cursor.execute('SELECT 1')  # Basit bir test sorgusu
                cursor.close()
                app.logger.info("Veritabanı bağlantısı başarılı!")
        except Exception as e:
            app.logger.error(f"Veritabanı bağlantısı hatası: {str(e)}")

        # Veritabanı bağlantı testini uygulama başlatıldığında yap

    test_db_connection()


    # 404 Hatası için özel mesaj
    @app.errorhandler(404)
    def page_not_found(e):
        # Bu satırda hata logunu yazıyoruz
        app.logger.error("404 Hatası: Sayfa bulunamadı!")
        return jsonify({"msg": "Sayfa bulunamadı!"}), 404

    # 401 Hatası için özel mesaj
    @app.errorhandler(401)
    def unauthorized_error(e):
        # Hata logunu yazıyoruz
        app.logger.error(f"401 Hatası: Yetkisiz erişim - {str(e)}")
        return jsonify({"msg": "Yetkisiz erişim!"}), 401

    # 500 Hatası için özel mesaj
    @app.errorhandler(500)
    def internal_error(e):
        # Bu satırda hata logunu yazıyoruz
        app.logger.error(f"500 Hatası: Sunucu hatası - {str(e)}")
        return jsonify({"msg": "Sunucu hatası! Lütfen tekrar deneyin."}), 500

    # 403 Hatası için özel mesaj
    @app.errorhandler(403)
    def forbidden(e):
        # Bu satırda hata logunu yazıyoruz
        app.logger.error(f"403 Hatası: Erişim reddedildi - {str(e)}")
        return jsonify({"msg": "Erişim reddedildi!"}), 403

    # 405 Hatası için özel mesaj
    @app.errorhandler(405)
    def method_not_allowed(e):
        # Bu satırda hata logunu yazıyoruz
        app.logger.error(f"405 Hatası: Yöntem engellendi - {str(e)}")
        return jsonify({"msg": "Geçersiz yöntem!"}), 405

    # 400 Hatası için özel mesaj
    @app.errorhandler(400)
    def bad_request(e):
        # Bu satırda hata logunu yazıyoruz
        app.logger.error(f"400 Hatası: Geçersiz istek - {str(e)}")
        return jsonify({"msg": "Geçersiz istek!"}), 400
        # Flask log seviyesini DEBUG olarak ayarlıyoruz
        app.logger.setLevel(logging.DEBUG)
    return app


# Flask uygulamasını başlatıyoruz
app = create_app()

# Uygulama çalıştırma kodu
if __name__ == '__main__':
    app.run(debug=True)
