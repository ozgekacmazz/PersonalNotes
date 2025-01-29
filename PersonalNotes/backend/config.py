class Config:
    # Flask için genel ayarlar
    SECRET_KEY = "779cfda5d70f399121590b19dd2127dc"  # Flask uygulaması için gizli anahtar

    # JWT için ayarlar
    JWT_SECRET_KEY = "a6a9e42f78856f3a97e2e7385175546338486f1f58938f78b5f06bf7577cbd1f"  # JWT token oluşturmak ve doğrulamak için kullanılan anahtar
    JWT_TOKEN_LOCATION = ["headers"]  # Token'ın header'da aranmasını belirtir
    JWT_HEADER_NAME = "Authorization"  # Header'da token'ın bulunacağı isim
    JWT_HEADER_TYPE = "Bearer"  # Header'daki token'ın türü (örneğin: Bearer <token>)

    # MySQL bağlantı ayarları
    MYSQL_HOST = "localhost"  # Veritabanı sunucusu
    MYSQL_USER = "root"  # MySQL kullanıcı adı
    MYSQL_PASSWORD = "aslisu123."  # MySQL şifresi
    MYSQL_DB = "PersonalNotes"  # Kullanılacak veritabanı




