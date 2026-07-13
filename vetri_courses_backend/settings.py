"""
Django settings for vetri_courses_backend project.
This is a brand-new, standalone project — it does not touch EduStruc or any
other project's database, code, or files.

This single file works in BOTH environments automatically:
- Locally: uses MySQL (MySQL Workbench) — unchanged from before.
- On PythonAnywhere: uses SQLite (their free tier doesn't include MySQL or
  Postgres). SQLite is a single file on disk — genuinely fine for this
  project's scale (a handful of courses, occasional admin use, a mobile
  app hitting a read-mostly API).
The switch happens automatically based on the ON_PYTHONANYWHERE environment
variable, which we set directly in the WSGI configuration file over there
(never set on your local machine).
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Set to True only when running on PythonAnywhere (set in the WSGI config file there).
IS_PRODUCTION = os.environ.get("ON_PYTHONANYWHERE") == "true"

# --- SECURITY ---
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-9yf)04&ip0@xt==j^j-=^w%_cgu87_=0y1jgd^t82t(vxxd8e-",  # local dev fallback only
)

DEBUG = not IS_PRODUCTION

ALLOWED_HOSTS = ["*"] if not IS_PRODUCTION else [
    "haripriyar2303.pythonanywhere.com",  # update if your PythonAnywhere username differs
]

if IS_PRODUCTION:
    CSRF_TRUSTED_ORIGINS = ["https://haripriyar2303.pythonanywhere.com"]

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
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # must stay near the top
    "django.middleware.security.SecurityMiddleware",
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
# Locally: MySQL (MySQL Workbench). On PythonAnywhere: SQLite (single file,
# persists normally on their disk — no separate database service needed).
if IS_PRODUCTION:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
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
# PythonAnywhere serves static files via a mapping you configure in their
# "Web" tab (pointing a URL like /static/ at this STATIC_ROOT folder) —
# no whitenoise or extra packages needed, unlike the Render setup.
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# --- MEDIA FILES ---
# Plain folder, same idea locally and on PythonAnywhere — their disk
# persists normally, so uploaded course images/PDFs just stay put.
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- CORS ---
# Harmless to leave open for a mobile-only API; matters more if you add a web dashboard later.
CORS_ALLOW_ALL_ORIGINS = True

# --- DRF ---
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",  # public read-only API; the admin panel is separately protected by login
    ],
}

# --- LOGGING ---
# Makes production errors print to console (visible in PythonAnywhere's
# error log) instead of only trying to email admins (which we haven't set up).
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