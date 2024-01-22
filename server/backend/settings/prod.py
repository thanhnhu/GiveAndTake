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
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


############
# SECURITY #
############

# django not allow serve static files on Production
# can use whitenoise or proxy to other server
# DEBUG = bool(os.getenv('DJANGO_DEBUG', ''))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', SECRET_KEY)

# Set to your Domain here (eg. 'django-vue-template-demo.herokuapp.com')
ALLOWED_HOSTS = ['*']
