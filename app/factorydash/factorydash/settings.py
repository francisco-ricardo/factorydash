"""
Django settings for factorydash project.
"""

from pathlib import Path
import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment and Security
RAILWAY_ENVIRONMENT_NAME = os.getenv("RAILWAY_ENVIRONMENT_NAME", "development")
IS_PRODUCTION = (RAILWAY_ENVIRONMENT_NAME == "production")
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    if not IS_PRODUCTION:
        SECRET_KEY = 'django-insecure-qwba_g+u=^%nl2%p2ih(uzw%jwch6#8r2@z4)nth#e0o1y%mtk'
    else:
        raise ImproperlyConfigured("SECRET_KEY must be set in production. Check Railway variables.")
DEBUG = not IS_PRODUCTION
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Database configuration
DEFAULT_DB_CONFIG = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'factorydash',
    'USER': 'factorydash',
    'PASSWORD': 'factorydash',
    'HOST': 'postgres',
    'PORT': '5432',
}
DATABASE_URL = os.getenv('DATABASE_URL')
try:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL) if DATABASE_URL else DEFAULT_DB_CONFIG
    }
except ValueError as e:
    raise ImproperlyConfigured(f"Invalid DATABASE_URL: {e}")

# Persist connections for 10 minutes to reduce connection overhead
DATABASES['default']['CONN_MAX_AGE'] = 600

# Data retention policy
DATA_RETENTION_DAYS = int(os.getenv("DATA_RETENTION_DAYS", "2"))

# Celery configuration
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', CELERY_BROKER_URL)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'monitoring',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'factorydash.urls'
WSGI_APPLICATION = 'factorydash.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "{asctime} [{levelname}] {module} - {message}", "style": "{"},
        "simple": {"format": "[{levelname}] {message}", "style": "{"},
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "factorydash.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 3,
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {"handlers": ["file", "console"], "level": "INFO", "propagate": True},
        "factorydash": {"handlers": ["file", "console"], "level": "DEBUG", "propagate": False},
    },
}

# EOF
