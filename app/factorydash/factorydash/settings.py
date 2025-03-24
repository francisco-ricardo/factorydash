"""
Django settings for factorydash project.
"""

from pathlib import Path
import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from urllib.parse import urlparse

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

# Celery configuration
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
if not CELERY_BROKER_URL:
    raise ImproperlyConfigured("CELERY_BROKER_URL must be set.")
try:
    parsed_url = urlparse(CELERY_BROKER_URL)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise ImproperlyConfigured("CELERY_BROKER_URL must be a valid URL (e.g., redis://host:port)")
except ValueError as e:
    raise ImproperlyConfigured(f"Invalid CELERY_BROKER_URL: {e}")

CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", CELERY_BROKER_URL)
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Fetch and validate LOAD_NIST_DATA_SCHEDULE_SECONDS
DEFAULT_LOAD_NIST_DATA_SCHEDULE_SECONDS = 3.0
LOAD_NIST_DATA_SCHEDULE_SECONDS = os.getenv('LOAD_NIST_DATA_SCHEDULE_SECONDS', str(DEFAULT_LOAD_NIST_DATA_SCHEDULE_SECONDS))
try:
    LOAD_NIST_DATA_SCHEDULE_SECONDS = float(LOAD_NIST_DATA_SCHEDULE_SECONDS)
    if LOAD_NIST_DATA_SCHEDULE_SECONDS <= 0:
        raise ValueError("LOAD_NIST_DATA_SCHEDULE_SECONDS must be a positive number")
except ValueError as e:
    raise ValueError(f"Invalid LOAD_NIST_DATA_SCHEDULE_SECONDS: {e}")

# Fetch and validate UPDATE_DASHBOARD_SCHEDULE_SECONDS
DEFAULT_UPDATE_DASHBOARD_SCHEDULE_SECONDS = 5.0
UPDATE_DASHBOARD_SCHEDULE_SECONDS = os.getenv("UPDATE_DASHBOARD_SCHEDULE_SECONDS", str(DEFAULT_UPDATE_DASHBOARD_SCHEDULE_SECONDS))
try:
    UPDATE_DASHBOARD_SCHEDULE_SECONDS = float(UPDATE_DASHBOARD_SCHEDULE_SECONDS)
    if UPDATE_DASHBOARD_SCHEDULE_SECONDS <= 0:
        raise ValueError("UPDATE_DASHBOARD_SCHEDULE_SECONDS must be a positive number")
except ValueError as e:
    raise ValueError(f"Invalid UPDATE_DASHBOARD_SCHEDULE_SECONDS: {e}")

# Fetch and validate CLEANUP_OLD_DATA_SCHEDULE_HOURS
DEFAULT_CLEANUP_OLD_DATA_SCHEDULE_HOURS = 1
CLEANUP_OLD_DATA_SCHEDULE_HOURS = os.getenv("CLEANUP_OLD_DATA_SCHEDULE_HOURS", str(DEFAULT_CLEANUP_OLD_DATA_SCHEDULE_HOURS))
try:
    CLEANUP_OLD_DATA_SCHEDULE_HOURS = int(CLEANUP_OLD_DATA_SCHEDULE_HOURS)
    if CLEANUP_OLD_DATA_SCHEDULE_HOURS <= 0:
        raise ValueError("CLEANUP_OLD_DATA_SCHEDULE_HOURS must be a positive number")
except ValueError as e:
    raise ValueError(f"Invalid CLEANUP_OLD_DATA_SCHEDULE_HOURS: {e}")

# Fetch and validate DATA_RETENTION_DAYS
DEFAULT_DATA_RETENTION_DAYS = 2
DATA_RETENTION_DAYS = os.getenv("DATA_RETENTION_DAYS", str(DEFAULT_DATA_RETENTION_DAYS))
try:
    DATA_RETENTION_DAYS = int(DATA_RETENTION_DAYS)
    if DATA_RETENTION_DAYS <= 0:
        raise ValueError("DATA_RETENTION_DAYS must be a positive integer")        
except ValueError as e:
    raise ValueError(f"Invalid DATA_RETENTION_DAYS: {e}")


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
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'factorydash.urls'
WSGI_APPLICATION = 'factorydash.wsgi.application'
ASGI_APPLICATION = 'factorydash.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [CELERY_BROKER_URL],
        },
    },
}

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
