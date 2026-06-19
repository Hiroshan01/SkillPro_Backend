import os
from datetime import timedelta
from pathlib import Path

from corsheaders.defaults import default_headers
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# --- Basic settings ---
SECRET_KEY = os.getenv("SECRET_KEY", "your-dev-secret-key")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    host.strip() for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host.strip()
]

# --- Application definition ---
INSTALLED_APPS = [
    # Project apps
    "users",
    "courses",
    "enrollments",
    "events",
    "inquiries",
    "notifications",
    "certificate",
    # Django built-in
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "knox",
    "corsheaders",
    # Celery periodic tasks (if you use django-celery-beat)
    # "django_celery_beat",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "application.urls"

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

WSGI_APPLICATION = "application.wsgi.application"


# --- Database (MySQL) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "3306"),
        # Remove OPTIONS block unless you specifically need a custom config file
    }
}


# --- Password validation ---
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- Internationalization ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Colombo")
USE_I18N = True
USE_TZ = True


# --- REST Framework + Knox ---
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_AUTHENTICATION_CLASSES": ["knox.auth.TokenAuthentication"],
}
REST_KNOX = {
    "TOKEN_TTL": timedelta(hours=10),
    "TOKEN_LIMIT_PER_USER": None,
}


# --- CORS ---
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL_ORIGINS", "False") == "True"
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]
CORS_ALLOW_HEADERS = list(default_headers) + ["X-Sector", "X-Property"]


# --- Static/Media Files (local or S3/Spaces, auto-switch based on .env) ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

USE_SPACES = os.getenv("USE_SPACES", "False") == "True"

if USE_SPACES:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"
    AWS_ACCESS_KEY_ID = os.getenv("SPACES_KEY")
    AWS_SECRET_ACCESS_KEY = os.getenv("SPACES_SECRET")
    AWS_STORAGE_BUCKET_NAME = os.getenv("SPACES_BUCKET")
    AWS_S3_ENDPOINT_URL = f"https://{os.getenv('SPACES_ENDPOINT')}"
    AWS_S3_REGION_NAME = os.getenv("SPACES_REGION")
    AWS_LOCATION = os.getenv("SPACES_LOCATION", "").strip("/") or ""
    AWS_DEFAULT_ACL = "public-read"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_QUERYSTRING_AUTH = False

    if AWS_LOCATION:
        MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.{os.getenv('SPACES_ENDPOINT')}/{AWS_LOCATION}/"
    else:
        MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.{os.getenv('SPACES_ENDPOINT')}/"
else:
    MEDIA_ROOT = BASE_DIR / "media"
    MEDIA_URL = "/media/"


# --- Email (update if you use SMTP or third party like Brevo/Sendgrid) ---
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@yourdomain.com")
# Add custom config if you use a third-party email service (see docs)


# --- Primary Key Field ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"
