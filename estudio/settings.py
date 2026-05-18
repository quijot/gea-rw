import logging
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS if not h.startswith(("127", "localhost"))]

INSTALLED_APPS = [
    "gea.apps.GeaConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "nested_admin",
    "dynamic_preferences",
    "django_extensions",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_tomselect",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_tomselect.middleware.TomSelectMiddleware",
]

ROOT_URLCONF = "estudio.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "dynamic_preferences.processors.global_preferences",
                "django_tomselect.context_processors.tomselect",
            ],
        },
    },
]

WSGI_APPLICATION = "estudio.wsgi.application"

DATABASES = {"default": {**env.db("DATABASE_URL"), "CONN_MAX_AGE": 500}}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

LOGIN_REDIRECT_URL = "home"

CRISPY_ALLOWED_TEMPLATE_PACKS = ["bootstrap5"]
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_FAIL_SILENTLY = not DEBUG

DYNAMIC_PREFERENCES = {
    "REGISTRY_MODULE": "preferences",
    "ADMIN_ENABLE_CHANGELIST_FORM": False,
}

CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
}

TOMSELECT = {"DEFAULT_CSS_FRAMEWORK": "bootstrap5"}

# django-tomselect emite warnings repetitivos cuando label_field es un campo virtual
# (no DB) — funcionalmente correcto pero ruidoso. Subir el nivel a ERROR.
logging.getLogger("django_tomselect.autocompletes").setLevel(logging.ERROR)
logging.getLogger("django_tomselect.widgets").setLevel(logging.ERROR)

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": env("DJANGO_LOG_LEVEL", default="INFO"),
            },
        },
    }
