from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager

# Flask-MYSQLdb için MySQL uzantısını başlat
mysql = MySQL()
def init_app(app):
    mysql.init_app(app)

jwt = JWTManager()  # JWTManager objesini oluştur


