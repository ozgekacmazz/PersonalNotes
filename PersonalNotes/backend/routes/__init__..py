from flask import Flask
from config import Config
from extensions import mysql
from routes.users import users_bp
from routes.notes import notes_bp
from routes.tasks import tasks_bp
from routes.projects import projects_bp
from routes.tags import tags_bp


def create_app():
    # Flask uygulamasını oluştur
    app = Flask(__name__)

    # Konfigürasyonu yükle
    app.config.from_object(Config)

    # Uzantıları başlat
    mysql.init_app(app)

    # Blueprint'leri kaydet
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(notes_bp, url_prefix='/notes')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(projects_bp, url_prefix='/projects')
    app.register_blueprint(tags_bp, url_prefix='/tags')

    # Ana sayfa route'u
    @app.route('/')
    def home():
        return "Kişisel Notlar API'sine hoş geldiniz!"

    return app
