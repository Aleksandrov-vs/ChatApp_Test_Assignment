import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False) == 'True'

if DEBUG:
    import socket
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] +\
                   ["127.0.0.1", ]

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = "login"

# Application definition

include(
    'components/installed_apps.py',
)

include(
    'components/middleware.py',
)

include(
    'components/logging_config.py',
)

ROOT_URLCONF = 'config.urls'

include(
    'components/templates.py',
)

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

include(
    'components/database.py',
)

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

include(
    'components/auth_password_validators.py',
)

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

if DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, './static/')
    STATIC_DIR = os.path.join(BASE_DIR, './static')
else:
    STATIC_ROOT = os.path.join(BASE_DIR, './static/')
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

include(
    'components/celery_config.py',
)

include(
    'components/chat_api_config.py',
)
