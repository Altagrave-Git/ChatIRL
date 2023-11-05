from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = [
    os.environ.get('ALLOWED_HOSTS1'),
    os.environ.get('ALLOWED_HOSTS2'),
    os.environ.get('ALLOWED_HOSTS3'),
    'localhost'
]

INSTALLED_APPS = [
    'daphne',
    'channels',
    'corsheaders',
    'rest_framework',
    'users.apps.UsersConfig',
    'chat.apps.ChatConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

if DEBUG:
    CORS_ALLOWED_ORIGINS = [
        'http://127.0.0.1:3000',
        'http://localhost:3000',
        'https://turcotte.tech',
        'https://www.turcotte.tech',
        'https://api.turcotte.tech',
        'https://echonetwork.app',
        'https://www.echonetwork.app',
    ]

else:
    CORS_ALLOWED_ORIGINS = [
        'https://turcotte.tech',
        'https://www.turcotte.tech',
        'https://api.turcotte.tech',
        'https://echonetwork.app',
        'https://www.echonetwork.app',
    ]

CORS_ALLOW_CREDENTIALS = True

# CSRF_COOKIE_NAME = "csrftoken"
# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_HTTPONLY = True
# CSRF_COOKIE_SAMESITE = None

# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_HTTPONLY = True
# SESSION_COOKIE_SAMESITE = None

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'main.wsgi.application'

ASGI_APPLICATION = 'main.asgi.application'

DATABASES = {
    "default": {
        "ENGINE": os.environ['ENGINE'],
        "NAME": os.environ['NAME'],
        "USER": os.environ['USER'],
        "PASSWORD": os.environ['PASSWORD'],
        "HOST": os.environ['HOST'],
        "PORT": "",
    }
}

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

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/media/'

if DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    MEDIA_ROOT = os.environ.get('MEDIA_ROOT')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

LOGOUT_REDIRECT_URL = 'login'

LOGIN_URL = 'login'