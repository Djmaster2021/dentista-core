# config/settings/dev.py
from .base import *
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent  # raíz del proyecto
load_dotenv(BASE_DIR / ".env")  # <-- lee .env del repo

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "dentista"),
        "USER": os.getenv("DB_USER", "dentyx"),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "3307"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


import dj_database_url

# Dev overrides
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Email en consola (para ver el enlace de reset en el terminal)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "Dentyx <no-reply@dentyx.local>"

LOGOUT_REDIRECT_URL = "login"  # o "/" o "dashboard"

# (Opcional) CORS extra en dev
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
