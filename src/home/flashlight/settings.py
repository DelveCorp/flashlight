"""
Django settings for flashlight project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""


# Environment variables used in this settings.py:
# 
# FLASHLIGHT_SECRET_KEY: Secret key for the Django application. Default: Generated random key.
# FLASHLIGHT_DEBUG: Boolean flag to enable/disable debug mode. Default: 'False'.
# FLASHLIGHT_ALLOWED_HOSTS: Comma-separated list of allowed hostnames. Default: '127.0.0.1,localhost'.
# FLASHLIGHT_INTERNAL_IPS: Comma-separated list of internal IPs for debugging. Default: '127.0.0.1'.
# FLASHLIGHT_STATIC_URL: URL for serving static files. Default: 'static/'.
# FLASHLIGHT_STATIC_ROOT: Directory for collecting static files. Default: 'staticfiles'.
# FLASHLIGHT_LOG_LEVEL: Logging level for the application. Default: 'INFO'.
# FLASHLIGHT_MEDIA_ROOT: Directory for storing media files. Default: 'uploads/'.
# FLASHLIGHT_MEDIA_URL: URL for serving media files. Default: 'uploads/'.
# FLASHLIGHT_AUTORELOAD: Boolean flag to enable/disable autoreload. Default: 'False'.
# FLASHLIGHT_SERVER_HOST: Hostname for the server. Default: '127.0.0.1'.
# FLASHLIGHT_SERVER_PORT: Port for the server. Default: 8000.
# FLASHLIGHT_SERVER_LOG_STDOUT: Boolean flag to enable/disable logging to stdout. Default: 'True'.
# FLASHLIGHT_MAX_REQUEST_BODY_SIZE: Maximum request body size. Default: 104857600.
# FLASHLIGHT_MAX_REQUEST_HEADER_SIZE: Maximum request header size. Default: 512000.
# FLASHLIGHT_SSL_PRIVATE_KEY: Path to the SSL private key file. Default: None.
# FLASHLIGHT_SSL_CERTIFICATE: Path to the SSL certificate file. Default: None.
# FLASHLIGHT_SSL_MODULE: SSL module to use. Default: 'builtin'.
# FLASHLIGHT_SOCKET_TIMEOUT: Socket timeout duration. Default: 10.
# FLASHLIGHT_SOCKET_QUEUE_SIZE: Socket queue size. Default: 5.
# FLASHLIGHT_ACCEPTED_QUEUE_TIMEOUT: Accepted queue timeout duration. Default: 10.
# FLASHLIGHT_SERVER_MAX_THREADS: Maximum number of server threads. Default: 20.
# FLASHLIGHT_ENABLE_EXTRACTIONS_ON_CREATE: Boolean flag to enable/disable extractions on create. Default: 'True'.
# FLASHLIGHT_ENABLE_PROCESSORSS_ON_CREATE: Boolean flag to enable/disable processors on create. Default: 'True'.
# FLASHLIGHT_ENABLE_EXTRACTIONS_ON_UPDATE: Boolean flag to enable/disable extractions on update. Default: 'True'.
# FLASHLIGHT_ENABLE_PROCESSORSS_ON_UPDATE: Boolean flag to enable/disable processors on update. Default: 'True'.
# FLASHLIGHT_STRICT_VALIDATION: Boolean flag to enable/disable strict validation. Default: 'False'.
# FLASHLIGHT_DOCUMENTATION_DIRECTORY: Directory for storing documentation. Default: 'doc'.
# FLASHLIGHT_Q_CLUSTER_NAME: Name of the Django Q cluster. Default: 'DjangORM'.
# FLASHLIGHT_Q_CLUSTER_CATCH_UP: Boolean flag to enable/disable catch-up for the Q cluster. Default: 'False'.
# FLASHLIGHT_Q_CLUSTER_WORKERS: Number of workers for the Q cluster. Default: 2.
# FLASHLIGHT_Q_CLUSTER_TIMEOUT: Timeout for the Q cluster. Default: 90.
# FLASHLIGHT_Q_CLUSTER_RETRY: Retry interval for the Q cluster. Default: 120.
# FLASHLIGHT_Q_CLUSTER_QUEUE_LIMIT: Queue limit for the Q cluster. Default: 50.
# FLASHLIGHT_Q_CLUSTER_BULK: Bulk size for the Q cluster. Default: 10.
# FLASHLIGHT_Q_CLUSTER_POLL: Poll interval for the Q cluster. Default: 1.
# FLASHLIGHT_Q_CLUSTER_ORM: ORM for the Q cluster. Default: 'default'.
# FLASHLIGHT_PYTHON_VERSION: Python version to use. Default: '3.13.1'.
# FLASHLIGHT_SERVICE_INTERVAL: Interval for the service commands. Default: 5.

# Note: Please keep this list up to date with any new environment variables added to the settings.

import os
import sys
import json
from pathlib import Path
import logging.config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: CHANGE THIS: keep the secret key used in production secret!
from django.core.management.utils import get_random_secret_key

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('FLASHLIGHT_SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('FLASHLIGHT_DEBUG', 'False') == 'True'

# List of allowed hostnames
ALLOWED_HOSTS = os.getenv('FLASHLIGHT_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# List of internal IPs for debugging
INTERNAL_IPS = os.getenv('FLASHLIGHT_INTERNAL_IPS', '127.0.0.1').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',  # Admin site
    'django.contrib.auth',  # Authentication framework
    'django.contrib.contenttypes',  # Content types framework
    'django.contrib.sessions',  # Session framework
    'django.contrib.messages',  # Messaging framework
    'django.contrib.staticfiles',  # Static files handling
    'django_extensions',  # Django extensions
    'whitenoise',  # WhiteNoise for serving static files
    'rest_framework',  # Django REST framework
    'django_bootstrap5',  # Bootstrap 5 integration
    'django_q',  # Django Q for task queues
    'users',  # Custom user app
    'events',  # Events app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Security middleware
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session middleware
    'django.middleware.common.CommonMiddleware',  # Common middleware
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection middleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentication middleware
    'django.contrib.messages.middleware.MessageMiddleware',  # Messaging middleware
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise middleware for static files
]

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')  # Debug toolbar for development
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")  # Debug toolbar middleware

# Root URL configuration
ROOT_URLCONF = 'flashlight.urls'

# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Template backend
        'DIRS': [ BASE_DIR / 'templates' ],  # Template directories
        'APP_DIRS': True,  # Enable app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Debug context processor
                'django.template.context_processors.request',  # Request context processor
                'django.contrib.auth.context_processors.auth',  # Auth context processor
                'django.contrib.messages.context_processors.messages',  # Messages context processor
                'events.context_processors.settings_context',  # Custom settings context processor
                'django.template.context_processors.media',  # Media context processor
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'flashlight.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            "timeout": 120, 
            "init_command": "PRAGMA journal_mode=WAL;", 
            "transaction_mode": "IMMEDIATE"), 
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # User attribute similarity validator
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Minimum length validator
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Common password validator
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Numeric password validator
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

# Internationalization settings
LANGUAGE_CODE = 'en-us'  # Language code
TIME_ZONE = 'UTC'  # Time zone
USE_I18N = True  # Enable internationalization
USE_TZ = True  # Enable timezone support


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Static files settings
STATIC_URL = os.getenv('FLASHLIGHT_STATIC_URL', 'static/')  # Static URL
STATIC_ROOT = Path(os.getenv('FLASHLIGHT_STATIC_ROOT', BASE_DIR / "staticfiles"))
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration
LOGGING_CONFIG = None
LOG_LEVEL = os.getenv('FLASHLIGHT_LOG_LEVEL', 'INFO')
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "verbose": {
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": '%(levelname)s %(name)s %(asctime)s %(module)s %(lineno)s %(process)d %(thread)d %(message)s',
            },
            "simple": {
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(levelname)s %(message)s",
            },
        },
        "handlers": {
            "file": {
                "level": LOG_LEVEL,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": BASE_DIR / "log" / f"{os.getpid()}-{sys.argv[1]}.log",
                "mode": "a",
                "maxBytes": 5242880,
                "backupCount": 10,
                "formatter": "verbose",
                # "delay": True,
            },
            "console": {
                "class": "logging.StreamHandler",
                "level": LOG_LEVEL,
                "formatter": "simple",
            },
        },
        "loggers": {
            "flashlight": {
                "handlers": ["file"],
                "level": LOG_LEVEL,
            },
            "": {
                "handlers": ["file", "console"],
                "level": LOG_LEVEL,
            },
        },
    }
)


# Custom user model
AUTH_USER_MODEL = "users.User"

# Authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
# This PAGE_SIZE really only helps the DRF browsable API.
# Submitting a Query does not respect this and will return
# the results as per your query.

# Django REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',  # Default pagination class
    'PAGE_SIZE': 100,  # Default page size
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',  # Basic authentication
        'rest_framework.authentication.SessionAuthentication',  # Session authentication
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Default permission class
        'events.permissions.IsOwner',  # Custom permission class
    ],
}

# Media files settings
MEDIA_ROOT = Path(os.getenv('FLASHLIGHT_MEDIA_ROOT', BASE_DIR / "uploads/"))
MEDIA_URL = os.getenv('FLASHLIGHT_MEDIA_URL', "uploads/")  # Media URL

# Flashlight-specific settings
FLASHLIGHT_AUTORELOAD = os.getenv('FLASHLIGHT_AUTORELOAD', 'False') == 'True'
FLASHLIGHT_SERVER_HOST = os.getenv('FLASHLIGHT_SERVER_HOST', '127.0.0.1')
FLASHLIGHT_SERVER_PORT = int(os.getenv('FLASHLIGHT_SERVER_PORT', 8000))
FLASHLIGHT_SERVER_LOG_STDOUT = os.getenv('FLASHLIGHT_SERVER_LOG_STDOUT', 'True') == 'True'
FLASHLIGHT_MAX_REQUEST_BODY_SIZE = int(os.getenv('FLASHLIGHT_MAX_REQUEST_BODY_SIZE', 104857600))
FLASHLIGHT_MAX_REQUEST_HEADER_SIZE = int(os.getenv('FLASHLIGHT_MAX_REQUEST_HEADER_SIZE', 512000))
FLASHLIGHT_SSL_PRIVATE_KEY = os.getenv('FLASHLIGHT_SSL_PRIVATE_KEY', None)
FLASHLIGHT_SSL_CERTIFICATE = os.getenv('FLASHLIGHT_SSL_CERTIFICATE', None)
FLASHLIGHT_SSL_MODULE = os.getenv('FLASHLIGHT_SSL_MODULE', 'builtin')
FLASHLIGHT_SOCKET_TIMEOUT = int(os.getenv('FLASHLIGHT_SOCKET_TIMEOUT', 10))
FLASHLIGHT_SOCKET_QUEUE_SIZE = int(os.getenv('FLASHLIGHT_SOCKET_QUEUE_SIZE', 5))
FLASHLIGHT_ACCEPTED_QUEUE_TIMEOUT = int(os.getenv('FLASHLIGHT_ACCEPTED_QUEUE_TIMEOUT', 10))
FLASHLIGHT_SERVER_MAX_THREADS = int(os.getenv('FLASHLIGHT_SERVER_MAX_THREADS', 20))

FLASHLIGHT_ENABLE_EXTRACTIONS_ON_CREATE = os.getenv('FLASHLIGHT_ENABLE_EXTRACTIONS_ON_CREATE', 'True') == 'True'
FLASHLIGHT_ENABLE_PROCESSORSS_ON_CREATE = os.getenv('FLASHLIGHT_ENABLE_PROCESSORSS_ON_CREATE', 'True') == 'True'
FLASHLIGHT_ENABLE_EXTRACTIONS_ON_UPDATE = os.getenv('FLASHLIGHT_ENABLE_EXTRACTIONS_ON_UPDATE', 'True') == 'True'
FLASHLIGHT_ENABLE_PROCESSORSS_ON_UPDATE = os.getenv('FLASHLIGHT_ENABLE_PROCESSORSS_ON_UPDATE', 'True') == 'True'
FLASHLIGHT_STRICT_VALIDATION = os.getenv('FLASHLIGHT_STRICT_VALIDATION', 'False') == 'True'

FLASHLIGHT_DOCUMENTATION_DIRECTORY = BASE_DIR.joinpath(os.getenv('FLASHLIGHT_DOCUMENTATION_DIRECTORY', 'doc'))

FLASHLIGHT_EXTRACTION_MAP = {
    'json': json.loads,
    'apache': 'events.parsers.apache',
    'csv': 'events.parsers.csv',
    'xml': 'xmltodict.parse',
}

FLASHLIGHT_PROCESSOR_MAP = {}

FLASHLIGHT_NAV_MENU = {
    "Flashlight": {
        "explore": "explore",
    },
}

FLASHLIGHT_SEARCH_COMMANDS = {
    # Generic search/transform operations
    'autocast': 'events.search_commands.autocast',
    'chart': 'events.search_commands.chart',
    'dedup': 'events.search_commands.dedup',
    'distinct': 'events.search_commands.distinct',
    'drop_fields': 'events.search_commands.drop_fields',
    'echo': 'events.search_commands.echo',
    'ensure_list': 'events.search_commands.ensure_list',
    'eval': 'events.search_commands.eval',
    'event_split': 'events.search_commands.event_split',
    'events_to_context': 'events.search_commands.events_to_context',
    'explode': 'events.search_commands.explode',
    'explode_timestamp': 'events.search_commands.explode_timestamp',
    'fake_data': 'events.search_commands.fake_data',
    'filter': 'events.search_commands.filter',
    'head': 'events.search_commands.head',
    'join': 'events.search_commands.join',
    'make_events': 'events.search_commands.make_events',
    'mark_timestamp': 'events.search_commands.mark_timestamp',
    'merge': 'events.search_commands.merge',
    'read_file': 'events.search_commands.read_file',
    'rename': 'events.search_commands.rename',
    'replace': 'events.search_commands.replace',
    'request': 'events.search_commands.request',
    'resolve': 'events.search_commands.resolve',
    'rex': 'events.search_commands.rex',
    'run_query': 'events.search_commands.run_query',
    'search': 'events.search_commands.search',
    'select': 'events.search_commands.select',
    'set': 'events.search_commands.set',
    'sort': 'events.search_commands.sort',
    'sql_query': 'events.search_commands.sql_query',
    'stats': 'events.search_commands.stats',
    'table': 'events.search_commands.table',
    'transpose': 'events.search_commands.transpose',
    'value_list': 'events.search_commands.value_list',

    'qs_aggregate': 'events.search_commands.qs.aggregate',
    'qs_alias': 'events.search_commands.qs.alias',
    'qs_annotate': 'events.search_commands.qs.annotate',
    'qs_count': 'events.search_commands.qs.count',
    'qs_dates': 'events.search_commands.qs.dates',
    'qs_datetimes': 'events.search_commands.qs.datetimes',
    'qs_defer': 'events.search_commands.qs.defer',
    'qs_delete': 'events.search_commands.qs.delete',
    'qs_distinct': 'events.search_commands.qs.distinct',
    'qs_earliest': 'events.search_commands.qs.earliest',
    'qs_exclude': 'events.search_commands.qs.exclude',
    'qs_exists': 'events.search_commands.qs.exists',
    'qs_explain': 'events.search_commands.qs.explain',
    'qs_filter': 'events.search_commands.qs.filter',
    'qs_first': 'events.search_commands.qs.first',
    'qs_last': 'events.search_commands.qs.last',
    'qs_latest': 'events.search_commands.qs.latest',
    'qs_only': 'events.search_commands.qs.only',
    'qs_order_by': 'events.search_commands.qs.order_by',
    'qs_reverse': 'events.search_commands.qs.reverse',
    'qs_select_related': 'events.search_commands.qs.select_related',
    'qs_update': 'events.search_commands.qs.update',
    'qs_using': 'events.search_commands.qs.using',
    'qs_values': 'events.search_commands.qs.values',
    'qs_group_by': 'events.search_commands.qs.group_by',
    'qs_having': 'events.search_commands.qs.having',
    'qs_limit': 'events.search_commands.qs.limit',

    'dp_list': 'datapower.search_commands.dp_list',
    'dp_get_status': 'datapower.search_commands.get_status',
    'dp_get_config': 'datapower.search_commands.get_config',
    'dp_get_providers': 'datapower.search_commands.get_providers',
    'dp_get_cert_details': 'datapower.search_commands.get_cert_details',
    'dp_patch': 'datapower.search_commands.patch',
    'dp_export': 'datapower.search_commands.export',
    'dp_import': 'datapower.search_commands.dp_import',
    'dp_list_exports': 'datapower.search_commands.list_exports',
    'dp_parse_extLatency': 'datapower.search_commands.parse_extLatency'
}


# Django Q cluster settings
Q_CLUSTER = {
    'name': os.getenv('FLASHLIGHT_Q_CLUSTER_NAME', 'DjangORM'),
    'catch_up': os.getenv('FLASHLIGHT_Q_CLUSTER_CATCH_UP', 'False') == 'True',
    'workers': int(os.getenv('FLASHLIGHT_Q_CLUSTER_WORKERS', 2)),
    'timeout': int(os.getenv('FLASHLIGHT_Q_CLUSTER_TIMEOUT', 90)),
    'retry': int(os.getenv('FLASHLIGHT_Q_CLUSTER_RETRY', 120)),
    'queue_limit': int(os.getenv('FLASHLIGHT_Q_CLUSTER_QUEUE_LIMIT', 50)),
    'bulk': int(os.getenv('FLASHLIGHT_Q_CLUSTER_BULK', 10)),
    'poll': int(os.getenv('FLASHLIGHT_Q_CLUSTER_POLL', 1)),
    'orm': os.getenv('FLASHLIGHT_Q_CLUSTER_ORM', 'default')
}

python = BASE_DIR / 'python' / os.getenv('FLASHLIGHT_PYTHON_VERSION', '3.13.1') / 'python.exe'
syslog_script = BASE_DIR / 'utilities' / 'cli' / 'syslog-receiver.py'
# syslog_command = f'{python} {syslog_script} --server http://127.0.0.1:8000 --index datapower_logs --tcp-cert C:/Users/cliff/projects/mast3/build/assemble/etc/crypto/cert/mast.crt --tcp-key C:/Users/cliff/projects/mast3/build/assemble/etc/crypto/private/mast.key -u FLASHLIGHT_USER -p FLASHLIGHT_PASSWORD --line-ending linux --tcp --tcp-port 1514 --hostname 192.168.0.190 -vvvvvv'

FLASHLIGHT_SERVICE_COMMANDS = [
    str(BASE_DIR / 'fl.bat') + ' serve',
    str(BASE_DIR / 'fl.bat') + ' qcluster',
    # syslog_command,
]
FLASHLIGHT_SERVICE_INTERVAL = int(os.getenv('FLASHLIGHT_SERVICE_INTERVAL', 5))
