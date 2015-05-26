"""
Django settings for seared_quail project.
:Created: 4 May 2015
:Author: Lucas Connors

"""

import os

import seared_quail.settings_secret as secret

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TOP_DIR = os.path.dirname(BASE_DIR)
SECRET_KEY = secret.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ordered_model',
    'menu',
    'order',
    'restaurant',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'seared_quail.urls'
WSGI_APPLICATION = 'seared_quail.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'seared_quail',
        'USER': secret.DATABASE_USER,
        'PASSWORD': secret.DATABASE_PASSWORD,
        'HOST': secret.DATABASE_HOST,
        'PORT': secret.DATABASE_PORT,
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True

# Templates and static files (CSS, JavaScript, Images)
MEDIA_ROOT = os.path.join(TOP_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(TOP_DIR, 'static'),
)
TEMPLATE_DIRS = (
    os.path.join(TOP_DIR, 'templates'),
)

# Authentication
LOGIN_URL = '/login/'
