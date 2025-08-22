# config/settings/base.py
from pathlib import Path
from datetime import timedelta
import os

from dotenv import load_dotenv

# -------------------------------------------------------------------
# Paths & .env
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

# -------------------------------------------------------------------
# Core
# -------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "dev-insecure-key")  # override en prod
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()]

SITE_ID = 1

# -------------------------------------------------------------------
# Tema (opcional)
# -------------------------------------------------------------------
THEME = {
    "PRIMARY":   "#163832",
    "SECONDARY": "#235347",
    "SUCCESS":   "#8EB69B",
    "LIGHT":     "#DAF1DE",
    "DARK":      "#051F20",
}

# -------------------------------------------------------------------
# Apps
# -------------------------------------------------------------------
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # 3rd party
    "rest_framework",
    "drf_spectacular",
    "corsheaders",

    # Auth social (allauth)
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",

    # Local apps
    "apps.accounts",
    "apps.patients",
    "apps.services",
    "apps.appointments",
    "apps.legacy",
]

# -------------------------------------------------------------------
# Middleware (AccountMiddleware DEBE ir después de AuthenticationMiddleware)
# -------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",   # <-- requerido por allauth
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -------------------------------------------------------------------
# URLs / Templates
# -------------------------------------------------------------------
ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # <-- necesario para allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.theme",
            ],
        },
    },
]

# -------------------------------------------------------------------
# Auth (modelo, backends, allauth)
# -------------------------------------------------------------------
AUTH_USER_MODEL = "accounts.User"  # etiqueta de app 'accounts' (app label)

AUTHENTICATION_BACKENDS = [
    "apps.accounts.backends.EmailOrUsernameBackend",       # tu backend (username/email)
    "django.contrib.auth.backends.ModelBackend",           # respaldo
    "allauth.account.auth_backends.AuthenticationBackend", # requerido por allauth
]

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"          # a tu dashboard cuando esté
LOGOUT_REDIRECT_URL = "/login/"

# Nuevas claves (evita deprecations)
ACCOUNT_LOGIN_METHODS = {"email"}                         # o {"email","username"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_USERNAME_GENERATOR = None
ACCOUNT_EMAIL_VERIFICATION = "optional"                   # "mandatory" si quieres forzar verificación
# (si usas login por email únicamente, no necesitas username en formularios)

# Proveedores sociales (credenciales desde .env)
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
            "secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
            "key": "",
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    },
    "facebook": {
        "APP": {
            "client_id": os.getenv("FACEBOOK_APP_ID", ""),
            "secret": os.getenv("FACEBOOK_APP_SECRET", ""),
            "key": "",
        },
        "METHOD": "oauth2",
        "SCOPE": ["email"],
        "FIELDS": ["email", "name", "first_name", "last_name"],
    },
}

# -------------------------------------------------------------------
# Base de datos (base: sqlite; override en dev/prod para MySQL)
# -------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
# Si quieres usar MySQL aquí mismo (opcional):
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": os.getenv("DB_NAME", ""),
#         "USER": os.getenv("DB_USER", ""),
#         "PASSWORD": os.getenv("DB_PASSWORD", ""),
#         "HOST": os.getenv("DB_HOST", "127.0.0.1"),
#         "PORT": os.getenv("DB_PORT", "3306"),
#         "OPTIONS": {"charset": "utf8mb4"},
#     }
# }

# -------------------------------------------------------------------
# Passwords y auth
# -------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------------------------------------------------
# i18n
# -------------------------------------------------------------------
LANGUAGE_CODE = "es-mx"
TIME_ZONE = "America/Mexico_City"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# Static & media
# -------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------------------------------------------------
# DRF / OpenAPI
# -------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Dentista API",
    "DESCRIPTION": "API del consultorio dental",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# -------------------------------------------------------------------
# SimpleJWT
# -------------------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# -------------------------------------------------------------------
# CORS
# -------------------------------------------------------------------
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
