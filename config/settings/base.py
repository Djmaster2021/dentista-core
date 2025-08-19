from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-change-in-prod")

DEBUG = False  # En dev.py lo forzamos a True
DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps del proyecto
    "apps.accounts",
    "apps.patients",
    "apps.appointments",
    "apps.payments",
    "apps.treatments.apps.TreatmentsConfig",  # antes: apps.services (única entrada)
    "apps.portal",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ⬇️ Ajusta según tu modelo real:
AUTH_USER_MODEL = "accounts.User"  # Si tu clase es CustomUser => "accounts.CustomUser"

LANGUAGE_CODE = "es-mx"
TIME_ZONE = "America/Mexico_City"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "portal:patient_home"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
