""" Production Settings """

import os
import dj_database_url
from .dev import *

############
# DATABASE #
############
# Production database configuration
# In production, always use environment variables for security
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'NAME': os.environ.get('DB_NAME', 'giveandtake'),
        'USER': os.environ.get('DB_USER', 'giveandtake'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'giveandtake')
    }
}

############
# SECURITY #
############
# Production security settings
DEBUG = False  # Never enable debug in production
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# Set to your Domain here (eg. 'django-vue-template-demo.herokuapp.com')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Google Drive Authentication Setup from server Secret Files
SERVICE_ACCOUNT_FILE = os.environ.get('GOOGLE_SERVICE_ACCOUNT_FILE', '/etc/secrets/credentials.json')

# Cloudinary configuration for production
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

# Storage configuration for production
STORAGE = os.environ.get('STORAGE_TYPE', 'cloudinary')  # Default to cloudinary in production

# Google Drive configuration
SCOPES = ['https://www.googleapis.com/auth/drive']
DRIVEFOLDERID = os.environ.get('GOOGLE_DRIVE_FOLDER_ID', '1oFoOJg9fVsdtHkyfQS2Vph0asGDe1Sg2')
