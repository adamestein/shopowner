# Django settings for Booth Apps project.

import os
import sys

DEBUG = True                # Dev Setting

# DEBUG = False             # Prod Setting

# Override if necessary to migrate release databases
if bool(os.environ.get("RELEASE", False)):
    DEBUG = False

REMOTE_SERVER = False       # Local Setting
# REMOTE_SERVER = True      # Remote Setting

ADMINS = (
    ('Adam Stein', 'adam@csh.rit.edu'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hhincwe_shopowner',
        'USER': 'hhincwe_shopownr',
        'PASSWORD': 'ALNRj6uF',
        'HOST': 'mysql1209.ixwebhosting.com',
        'PORT': '3306',
    }
}

if DEBUG:
    DATABASES["default"]["HOST"] = "localhost"

if "test" in sys.argv:
    DATABASES["default"] = {'ENGINE': 'django.db.backends.sqlite3'}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['smeg.steinhome.net', ]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/home/stein/www/shopowner_static'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/shopowner_static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), '../public/static').replace('\\', '/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'qnajvv@#pkfuin*bzy4i52mr#hgg-k@ek+jhvc#qxcej8&-4p0'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../admintools/templates')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../inventory/templates'))
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.debug',
                'django.contrib.messages.context_processors.messages',
                'django_settings_export.settings_export',
                'common.context_processors.version'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ]
        }
    }
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'system.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'system.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'db_file_storage',
    'django_behave',
    'common',
    'inventory',
    'sales',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

if REMOTE_SERVER:
    # Needed to do formating for Python v2.6
    import locale
    locale.setlocale(locale.LC_ALL, '')

# Account URLs
LOGIN_URL = "/shopowner/accounts/login/"
LOGOUT_URL = "/shopowner/accounts/logout/"

# Use the Django Behave test runner so that we can run our normal unit tests in
# addition to BDD tests
TEST_RUNNER = 'django_behave.runner.DjangoBehaveTestSuiteRunner'

# To store images in database
DEFAULT_FILE_STORAGE = 'db_file_storage.storage.DatabaseFileStorage'

VERSION = "1.18"
