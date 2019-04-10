from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'SECRET_KEY'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'blog_backend',
        'USER': 'blog_backend',
        'PASSWORD': 'blog_backend',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# SMTP
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'user@yandex.ru'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_SSL = True

# Urls client
URL_CLIENT_CONFIRM_EMAIL = 'http://localhost:8000/confirm_email/'
