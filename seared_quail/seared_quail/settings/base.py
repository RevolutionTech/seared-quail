"""
:Created: 4 May 2015
:Author: Lucas Connors

"""

import os

from cbsettings import DjangoDefaults


class BaseSettings(DjangoDefaults):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    TOP_DIR = os.path.dirname(BASE_DIR)

    DEBUG = True
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

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(TOP_DIR, 'templates')],
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
    WSGI_APPLICATION = 'seared_quail.wsgi.application'

    # Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'seared_quail',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        },
    }

    # Internationalization
    TIME_ZONE = 'UTC'
    USE_L10N = True
    USE_TZ = True

    # Templates and static files (CSS, JavaScript, Images)
    MEDIA_ROOT = os.path.join(TOP_DIR, 'media')
    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        os.path.join(TOP_DIR, 'static'),
    )

    # Authentication
    LOGIN_URL = '/login/'
