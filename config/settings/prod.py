from .base import *
import dj_database_url
import os

DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",") if os.getenv("ALLOWED_HOSTS") else []

SECRET_KEY = os.getenv("SECRET_KEY")

DATABASES = {
    "default": dj_database_url.parse(os.getenv("DATABASE_URL", ""), conn_max_age=600, ssl_require=False)
}

# Seguridad típica prod (ajusta según tu entorno)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
