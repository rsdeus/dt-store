"""
Django settings for dtstore project.

Generated by 'django-admin startproject' using Django 1.11.18.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

from decouple import config
import dj_database_url
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

WSGI_APPLICATION='dtstore.wsgi.application'
ROOT_URLCONF='dtstore.urls'

DATABASES = {'default': {}}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # libs
    'widget_tweaks',
    'whitenoise',
    'easy_thumbnails',
    'import_export',
    # apps
    'core',
    'apps.accounts.apps.AccountsConfig',
    'apps.address.apps.AddressConfig',
    'apps.catalog.apps.CatalogConfig',
    'apps.checkout.apps.CheckoutConfig',
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

    'apps.checkout.middleware.cart_item_middleware',
]

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
                # apps
                'apps.catalog.context_processors.categories',
            ],
        },
    },
]


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

# auth
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_URL = 'logout'
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'apps.accounts.backends.ModelBackend',
)

# Email
EMAIL_HOST = 'nhanduti.com.br'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'contato@nhanduti.com.br'
EMAIL_HOST_PASSWORD = 'Jmascis82'
EMAIL_USE_SSL = True

# Messages
from django.contrib.messages import constants as messages_constants
MASSAGE_TAGS = {
    messages_constants.DEBUG: 'debug',
    messages_constants.INFO: 'info',
    messages_constants.SUCCESS: 'success',
    messages_constants.WARNING: 'warning',
    messages_constants.ERROR: 'danger',
}

PAGSEGURO_TOKEN = 'A3FD5C2DA0464EA9A597D4F7ADA1909A'
PAGSEGURO_EMAIL = 'rsdeus@gmail.com'
PAGSEGURO_SANDBOX = True

# SHIPPING METHODS CONFIG

FIXED_PRICE = 0.00

AVAILABLE_PICKUP_DAYS = (
    ('segunda', 'Segunda'),
    ('terça', 'Terça'),
)

# Period the order will be holded
PICKUP_DAYS_TIMEOUT = 3

# Period to post an order in mail
PERIOD_TO_POST_ORDER = 2

POSTAL_CODE_FROM = '13082752'

PICKUP_ADDRESS = 'Rua Mata da Tijuca, 46 - Bosque de Barão Geraldo - Campinas - SP'

# Medidas da embalagem para os correios em centímetros
FORMAT = 1
LENGTH = 15
WIDTH = 20
HEIGHT = 5

# Expire time setting for clear the left orders and carts in minutes
EXPIRE_TIME = 1

# PAYMENT METHODS CONFIG

BANK_DETAILS = {
    'Banco': '',
    'Agencia': '',
    'Tipo de Conta': '',
    'Conta': '',
    'CPF/CNPJ': '',
}

# Thumbnails
THUMBNAIL_ALIASES = {
    '': {
        'product_image': {'size': (285,160), 'crop': True},
    },
}

# Logging
'''LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'checkout.views': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'filename': os.path.join(BASE_DIR, 'checkout.views.log'),
        }
    },
    'loggers': {
        'checkout.views': {
            'handlers': ['checkout.views'],
            'level': 'DEBUG',
        }
    }
}'''

try:
    from .local_settings import *
except ImportError:
    django_heroku.settings(locals())
    DATABASES['default'] = dj_database_url.config()
    DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
