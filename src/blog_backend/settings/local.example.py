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

