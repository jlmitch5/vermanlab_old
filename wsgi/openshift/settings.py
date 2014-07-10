# -*- coding: utf-8 -*-
# Django settings for openshift project.
import imp, os

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))

ON_OPENSHIFT = False

# a setting to determine whether we are running on OpenShift
if 'OPENSHIFT_REPO_DIR' in os.environ:
    ON_OPENSHIFT = True

    dbpath = os.environ['OPENSHIFT_DATA_DIR']
    DEBUG = bool(os.environ.get('DEBUG', False))

    DB_NAME = os.environ['OPENSHIFT_APP_NAME']
    DB_USER = os.environ['OPENSHIFT_MYSQL_DB_USERNAME']
    DB_PASSWD = os.environ['OPENSHIFT_MYSQL_DB_PASSWORD']
    DB_HOST = os.environ['OPENSHIFT_MYSQL_DB_HOST']
    DB_PORT = os.environ['OPENSHIFT_MYSQL_DB_PORT']

    if DEBUG:
        print("WARNING: The DEBUG environment is set to True.")
else:
    ON_OPENSHIFT = False
    dbpath=PROJECT_DIR
    DEBUG = True

if ON_OPENSHIFT:
    # os.environ['OPENSHIFT_DB_*'] variables can be used with databases created
    # with rhc app cartridge add (see /README in this git repo)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': DB_NAME,               # Or path to database file if using sqlite3.
            'USER': DB_USER,               # Not used with sqlite3.
            'PASSWORD': DB_PASSWD,         # Not used with sqlite3.
            'HOST': DB_HOST,               # Set to empty string for localhost. Not used with sqlite3.
            'PORT': DB_PORT,               # Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': os.path.join(PROJECT_DIR, 'sqlite3.db'),  # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

ALLOWED_HOSTS = ['*']

ADMINS = (
    ('John Mitchell', 'jmitchel@redhat.com') 
)

if ON_OPENSHIFT:
    MEDIA_ROOT = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'to_be_added')
else:
    MEDIA_ROOT = os.path.join(PROJECT_DIR, '..', 'static/media') 

MEDIA_URL = '/to_be_added/'

if ON_OPENSHIFT:
    STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static')
else:
    STATIC_ROOT = os.path.join(PROJECT_DIR, '..', 'static')

STATIC_URL = '/static/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'rest_framework',
    'widget_tweaks',
    'upload_kernel',
    'schema_kernel',
    'diff_kernel',
    'pci_ids',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)







TIME_ZONE = 'America/New_York'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

default_keys = { 'SECRET_KEY': 'vm4rl5*ymb@2&d_(gc$gb-^twq9w(u69hi--%$5xrh!xk(t%hw' }

if ON_OPENSHIFT:
    imp.find_module('openshiftlibs')
    import openshiftlibs
    use_keys = openshiftlibs.openshift_secure(default_keys)
else:
    use_keys = default_keys

SECRET_KEY = use_keys['SECRET_KEY']

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

MANAGERS = ADMINS

DEBUG = True

TEMPLATE_DEBUG = DEBUG
