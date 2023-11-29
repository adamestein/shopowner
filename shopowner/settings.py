"""
Django settings for shopowner project.

Generated by 'django-admin startproject' using Django 1.11.29.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from os import path
import sys

# noinspection PyPackageRequirements
from decouple import config, Csv

from django.contrib.messages import constants as messages
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

# Add the 'apps' directory to the path since all code lives under there
sys.path.append(path.join(BASE_DIR, 'apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    'compressor',
    'dashing',
    'django_cleanup.apps.CleanupConfig',
    'widget_tweaks',

    # Apps
    'artifacts',
    'inventory',
    'library',
    'orders',
    'vendors'
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

ROOT_URLCONF = 'shopowner.urls'

TEMPLATES = [
    {
        'APP_DIRS': True,
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [path.normpath(path.join(BASE_DIR, 'templates'))],
        'OPTIONS': {
            'context_processors': [
                # Django context processors
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # 3rd Party processors
                'django_settings_export.settings_export'
            ],
        },
    },
]

WSGI_APPLICATION = 'shopowner.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'OPTIONS': {
            'init_command': 'SET sql_mode="STRICT_ALL_TABLES"'
        },
        'STORAGE_ENGINE': 'INNODB'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = path.abspath(path.join(BASE_DIR, 'static'))
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    path.abspath(path.join(BASE_DIR, 'public'))
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
]

# Uploaded files

MEDIA_URL = f'http://{config("MEDIA_HOST")}/files/'

# Account URLs

LOGOUT_REDIRECT_URL = '/'

# Version information

VERSION = '3.6.1'

# List of settings to export to templates (django-settings-export)

SETTINGS_EXPORT = [
    'DEBUG',
    'VERSION'
]

# Connect Bootstrap alerts to Django message tags

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }

# Compressor settings

COMPRESS_ENABLED = True

# Dashboard settings

DASHING = {
    'PERMISSION_CLASSES':  (
        'dashing.permissions.IsAuthenticated',
    )
}

# Production vs Development specific stuff

if DEBUG:
    INSTALLED_APPS.append('django_extensions')
else:
    # Logging handlers

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'filename': '/home/gina/logs/django.log'
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['file'],
                'level': 'WARNING',
                'propagate': True,
            },
        },
    }

# If running test suite use any settings from tests.py
if 'test' in sys.argv or 'test_coverage' in sys.argv:
    testing = True

    try:
        from .tests import *
    except ImportError:
        pass

    # Use SQLite3 databases for testing instead of MySQL because:
    #
    #   o faster to start, faster to run, no cleanup needed
    #   o multiple tests can run at the same time
    #   o no need to 'destroy' the test database when starting a new test if the previous test
    #     stopped before cleaning up
    #
    # Need to set this here since tests.py will have no idea what DATABASES is.
    DATABASES["default"] = {'ENGINE': 'django.db.backends.sqlite3', 'NAME': '/tmp/default.db'}
else:
    testing = False
