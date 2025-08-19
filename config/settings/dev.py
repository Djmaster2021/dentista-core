from .base import *
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE", "dentyx"),
        "USER": os.getenv("MYSQL_USER", "root"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD", "root"),
        "HOST": os.getenv("MYSQL_HOST", "127.0.0.1"),  # Docker MySQL mapeado a 3306
        "PORT": os.getenv("MYSQL_PORT", "3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8001", "http://localhost:8001"]
