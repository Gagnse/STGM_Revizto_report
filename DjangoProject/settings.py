"""
Django settings for DjangoProject project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-t@dfso$tn#=gfd+4@!juok9vbm$k1mo#1yh7t5w0z$ed9m&1u-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Add your app here - we'll create it in the next step
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DjangoProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # This points to your templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DjangoProject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # This points to your static files directory
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Revizto API Settings
REVIZTO_API_BASE_URL = "https://api.canada.revizto.com/v5/"

# These should be set in your environment variables for security
# You will need to provide these values
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6ImExMGM0YTJmMDRlNTljZWZjODVhYzE0NWVjODM4NGRlZGZiOWE2OTU1MWNlN2NjOWRkM2M2YWE2YTllODE2OTc3ZTc5ODVjZDUwMzE0OGZkIiwiaWF0IjoxNzQ2NjM4MTA4LjYyNjAxOSwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDY2MzgxMDguNjI2MDI0LCJleHAiOjE3NDY2NDE3MDguNTg5ODg4LCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.FqxoME7Aj5ZCfXtM9zKJH_1DO9fWZlRtk0ZkuuvwBt7pMDhiHy79Te1u09iP8ShBc6DFAYfByoTCsUyLhXIOeLCGWxswR64tDv5qKDjHv2K5hT4Gxe17lvz8K3P4OqPNjdZVx_t5KQoEMrMBa6s7qAXgSIINPWe9_uX2Oqk7HThwGzGWnIV745yfnl8JRP6eLFD5nz66dc_M5KYy6nDs5chjGD_9uZowiLEt8xfnY_gaFwTgwuUuDVasS5vj5GYSy_GF8EDu9_fnj_8-1q4YXM_tpSacPyrRM3tcb70VqZQtsoXTvCpWud-_HsItJVgbF7kePbMQWYH2ehHUSrjhAg"
REVIZTO_REFRESH_TOKEN = "def50200e75e1945e3b82663ac3ae84cac00f24cb78a3c2a8dcbd4c50740c4ce574827978e8fd454df714a7abe523be377927a61e1eb6310d6289f1d25c8fbc44f7770a4f3be3af5445eea5ab70cd0d45ab7c7b6b2af71ec8205407d100b7560b96135283f6f6b48de70170a0ae81d2d691471edfda9a6aeaf8bf09297f06bd370417bb9796c7d9a051c3277d4bde4fdaeac2afd5621cd853d313d98d81aaa5ba4d3c22f3cd6c24d60a2b821c5a27d137802635d2085163d8ddd52029538c49c0e318b7b0f27cb7eec1f44b46a513244920cd5ac29c74dd65f61d830be21a3d22b3256c664533f0518516719e1576ba2c2055a1b3887c6a4da3f7d8e99d3a89c84f8d4ac24ad66cae3f0d062265042ca27336d3a57c49bb28426f75157adbd652e5935e2f20d1bea41d68049820366f4a6179124e8ebc7a774ace45875e63d885fe219ced86b0720384e6c0d08754193ee0868c21402ddb0ef240f8718b3cbc64d680e91e4c8a78f8f3e3c0b1f5a801290127a70fa25f17f388ef10e98cfb05ab9f619bec11e20f2fe62a39855cefbeb9c24051b3a6f9f8558dd6d4131a9c19d2db64fc832150df1bf40d1c54d350b8062fb1732d37d78a4317aa807d60b2fd4cd8a4b0758a77d01757cd1a3bffb8503152a51d9c308238797d2e35fc44bb95e0b171a1aa206d9f6217054f9e896c6c0492d4eeb2a1351c3427d21b82ffe02637beb31c755a995c247236f0975d97424c2da64aa4c6c60c877e05da24ae465d301698bc192466c859420e663fa7a961fdd792171d9f65770322b0aa7c363d56d57b815cce852c3c3c56de7cb7796054f4409b8194a62d693773aade0"
REVIZTO_LICENCE_UUID = "2e38d742-c9ad-4d11-b5a8-c9b53e9bf517"
# For production, use environment variables instead
# import os
# REVIZTO_ACCESS_TOKEN = os.environ.get("REVIZTO_ACCESS_TOKEN")
# REVIZTO_REFRESH_TOKEN = os.environ.get("REVIZTO_REFRESH_TOKEN")


# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

# Session cookie settings
SESSION_COOKIE_NAME = 'sessionid'  # Default cookie name
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds (default)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Keep session when browser closes
SESSION_SAVE_EVERY_REQUEST = True  # Save the session on every request (important for reliable persistence)

# Debug logging configuration - add this to your LOGGING config
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'core': {  # Your app logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}