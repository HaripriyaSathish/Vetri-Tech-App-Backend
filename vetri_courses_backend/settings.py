"""
Django settings for vetri_courses_backend project.
This is a brand-new, standalone project — it does not touch EduStruc or any
other project's database, code, or files (it uses its own separate Neon
Postgres database, not EduStruc's Render database).

This single file works in BOTH environments automatically:
- Locally: uses MySQL (MySQL Workbench) — unchanged from before.
- On Render: uses PostgreSQL (via Neon), set through the DATABASE_URL
  environment variable in Render's dashboard.
The switch happens automatically based on whether DATABASE_URL is set
(only ever set on Render, never on your local machine).
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

IS_PRODUCTION = bool(os.environ.get("DATABASE_URL"))

# --- SECURITY ---
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-9yf)04&ip0@xt==j^j-=^w%_cgu87_=0y1jgd^t82t(vxxd8e-",  # local dev fallback only
)

DEBUG = not IS_PRODUCTION

ALLOWED_HOSTS = ["*"] if not IS_PRODUCTION else [
    "vetri-tech-app-backend.onrender.com",
]

if IS_PRODUCTION:
    CSRF_TRUSTED_ORIGINS = ["https://vetri-tech-app-backend.onrender.com"]
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# --- APPS ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "mobile_courses",
    "site_content",
]

if IS_PRODUCTION:
    INSTALLED_APPS += ["cloudinary_storage", "cloudinary"]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # must stay near the top
    "django.middleware.security.SecurityMiddleware",
]

if IS_PRODUCTION:
    MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")  # serves admin's CSS/JS in production

MIDDLEWARE += [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "vetri_courses_backend.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "vetri_courses_backend.wsgi.application"

# --- DATABASE ---
# Locally: MySQL (MySQL Workbench). On Render: PostgreSQL via Neon
# (a database genuinely separate from EduStruc's, avoiding the shared
# auth-table collision we hit when trying to reuse EduStruc's database).
if IS_PRODUCTION:
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.config(
            default=os.environ.get("DATABASE_URL"),
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("DB_NAME", "vetri_courses_db"),
            "USER": os.environ.get("DB_USER", "root"),
            "PASSWORD": os.environ.get("DB_PASSWORD", "Root123$"),
            "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
            "PORT": os.environ.get("DB_PORT", "3306"),
            "OPTIONS": {
                "charset": "utf8mb4",
            },
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# --- STATIC FILES ---
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# --- STATIC & MEDIA FILE STORAGE (Django 4.2+ STORAGES setting) ---
# Locally: plain filesystem storage (fine, MySQL Workbench dev setup).
# On Render: Cloudinary for media (genuinely persistent) + Whitenoise for
# static files. Using the modern STORAGES dict instead of the older
# DEFAULT_FILE_STORAGE/STATICFILES_STORAGE settings, since Django 5.2
# prioritizes STORAGES and the older settings weren't reliably honored.
MEDIA_URL = "/media/"
if IS_PRODUCTION:
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
        "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
        "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
    }
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
else:
    MEDIA_ROOT = BASE_DIR / "media"
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- CORS ---
CORS_ALLOW_ALL_ORIGINS = True

# --- DRF ---
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# --- LOGGING ---
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}