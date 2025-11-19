from datetime import timedelta
from pathlib import Path

from decouple import config

# ==============================================================
# BASE DIRECTORY
# ==============================================================

# Absolute path to the project root, used for building paths
# https://docs.python.org/3/library/pathlib.html#pathlib.Path.resolve
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ==============================================================
# SECURITY SETTINGS
# ==============================================================

# Secret key for Django. Keep it safe and never expose publicly.
# https://docs.djangoproject.com/en/5.2/ref/settings/#secret-key
SECRET_KEY = config("SECRET_KEY")

# Debug mode. Should be False in production.
# https://docs.djangoproject.com/en/5.2/ref/settings/#debug
DEBUG = config("DEBUG", default=False, cast=bool)

# Allowed hosts for HTTP requests
# https://docs.djangoproject.com/en/5.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# ==============================================================
# APPLICATION DEFINITION
# ==============================================================

# Django built-in apps
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Third-party apps
THIRD_PARTY_APPS = [
    "rest_framework",  # Django REST framework
    "corsheaders",  # Cross-Origin Resource Sharing support
    "rest_framework_simplejwt",  # JWT authentication
]

# Local project apps
LOCAL_APPS = ["apps.accounts"]

# Installed apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware stack
# CorsMiddleware must be placed before CommonMiddleware
# https://github.com/adamchainz/django-cors-headers#setup
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

ROOT_URLCONF = "config.urls"


# ==============================================================
# TEMPLATES
# ==============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Global templates directory
        "APP_DIRS": True,  # Load templates from apps automatically
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


# ==============================================================
# DATABASE CONFIGURATION
# ==============================================================

# SQLite used for development
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ==============================================================
# PASSWORD VALIDATION
# ==============================================================

# Validators to enhance password security
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ==============================================================
# INTERNATIONALIZATION
# ==============================================================

# https://docs.djangoproject.com/en/5.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ==============================================================
# STATIC FILES
# ==============================================================

# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = "static/"

# Default primary key field type for models
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ==============================================================
# CUSTOM USER MODEL
# ==============================================================

# Reference to custom user model
AUTH_USER_MODEL = "accounts.User"


# ==============================================================
# CORS CONFIGURATION
# ==============================================================

# Allowed origins for Cross-Origin requests (development only)
# https://github.com/adamchainz/django-cors-headers#cors_allowed_origins
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Allowed headers for CORS requests
# Includes default headers + CSRF and Authorization
# https://github.com/adamchainz/django-cors-headers#cors_allow_headers
CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "x-csrftoken",
    "accept",
    "origin",
    "user-agent",
    "accept-encoding",
    "accept-language",
]

# Allowed HTTP methods for CORS
# https://github.com/adamchainz/django-cors-headers#cors_allow_methods
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]


# ==============================================================
# SECURITY SETTINGS
# ==============================================================

# Browser security settings
# https://docs.djangoproject.com/en/5.2/ref/middleware/#security-middleware
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"


# ==============================================================
# JWT CONFIGURATION
# ==============================================================

# Simple JWT settings for REST API
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}
