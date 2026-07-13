"""
Django settings for vetri_courses_backend project.
This is a brand-new, standalone project — it does not touch EduStruc or any
other project's database, code, or files.

This single file works in BOTH environments automatically:
- Locally: uses MySQL (MySQL Workbench) — unchanged from before.
- On Render: uses PostgreSQL + a Persistent Disk for media files.
The switch happens automatically based on whether DATABASE_URL is set
(Render sets it automatically once you attach a Postgres instance;
it's never set on your local machine).
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Set to True automatically whenever this is running on Render
# (DATABASE_URL only ever exists in that environment).
IS_PRODUCTION = bool(os.environ.get("DATABASE_URL"))

# --- SECURITY ---
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-9yf)04&ip0@xt==j^j-=^w%_cgu87_=0y1jgd^t82t(vxxd8e-",  # local dev fallback only
)

DEBUG = not IS_PRODUCTION

ALLOWED_HOSTS = ["*"] if not IS_PRODUCTION else [
    "vetri-tech-app-backend.onrender.com",  # replace with your actual Render URL once created
]

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
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serves admin's CSS/JS in production
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
# Locally: MySQL (MySQL Workbench). On Render: PostgreSQL (Render doesn't
# offer managed MySQL — same reasoning as your EduStruc migration).
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
if IS_PRODUCTION:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- MEDIA FILES ---
# Locally: plain folder in the project (fine for local testing).
# On Render: a Persistent Disk mounted at /var/data, so uploaded course
# images/PDFs survive redeploys — Django's default FileSystemStorage (same
# one used locally) just points at a different, persistent folder. No
# third-party storage backend involved — Django Admin looks identical
# in both environments.
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