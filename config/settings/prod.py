from .base import *
import os

# Activa DEBUG solo con variable (para diagnosticar)
DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"

# Hosts para tus pruebas locales/LAN
ALLOWED_HOSTS = ["0.0.0.0", "127.0.0.1", "localhost"]
CSRF_TRUSTED_ORIGINS = ["http://0.0.0.0:8001", "http://127.0.0.1:8001"]

# ➜ NO reemplaces toda la lista; solo la extendemos con WhiteNoise al principio
BASE_MIDDLEWARE = MIDDLEWARE  # viene de base.py
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    *BASE_MIDDLEWARE,  # aquí ya están Session, Auth, Messages en el orden correcto
]

# WhiteNoise para estáticos en DEBUG=False
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
