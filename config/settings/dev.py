# config/settings/dev.py
from .base import *
import os
import dj_database_url

# Dev overrides
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Si está definida DATABASE_URL en el entorno, usa esa base (MySQL en tu caso)
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES["default"] = dj_database_url.parse(DATABASE_URL, conn_max_age=0)

# Email en consola (para ver el enlace de reset en el terminal)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@dentista.local"

# (Opcional) CORS extra en dev
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
