""" Production Settings """

import os
import dj_database_url
from .dev import *

############
# DATABASE #
############
DATABASES = {
    # 'default': dj_database_url.config(
    #     default=os.getenv('DATABASE_URL')
    # )
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'NAME': os.environ.get('DB_NAME', 'giveandtake'),
        'USER': os.environ.get('DB_USER', 'giveandtake'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'giveandtake'),
        'OPTIONS': {
            'charset': 'utf8mb4',  # Use Unicode
        }
    }
}


############
# SECURITY #
############
# Google Drive Authentication Setup from server Secret Files
SERVICE_ACCOUNT_FILE = '/etc/secrets/credentials.json'

# django not allow serve static files on Production
# can use whitenoise or proxy to other server
DEBUG = bool(os.getenv('DEBUG', ''))

SECRET_KEY = os.getenv('SECRET_KEY', SECRET_KEY)

# Set to your Domain here (eg. 'django-vue-template-demo.herokuapp.com')
ALLOWED_HOSTS = ['*']
