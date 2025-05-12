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
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_USERS_NAME', 'STGM_RAPPORT_REVIZTO_DB'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'sebas1234'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

DATABASE_ROUTERS = ['core.routers.ProjectRouter']

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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6IjM1MzkzODE4ZGFlMGNiZDJlOGQ2YTYxNzEyZjhmZjBiNDM2NDQ1ZDZiZDZkMTc5ZjdiMmMxMjlmZTJkNGU2NTM1ZGFkNzU5NzBiMjQ2ZmIyIiwiaWF0IjoxNzQ3MDc4MTI3LjAwODkwMywiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcwNzgxMjcuMDA4OTA4LCJleHAiOjE3NDcwODE3MjYuOTU1MzY2LCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.sOKB8QNqFWcJNqt_tXWyHDuFmLZEtAnpTHKPb4zs8gA4sDIP4dA0tLFfAAePDmHuYsipW0sfmpsM4O-Y2zHEFRDTodkIwmfjpTa5jt0Hc2gj1QsA2QTbGjps3to0Enr8E71JkpsqGO4v-dGjhxf_zNJ6FGCZxvaAGnVIi-HtJfZkVkPSn36Yh7yDRclWrFpGE6bEfgzAS6FaZQO5rO95jUVzIREorzGF78zN3bJKT51kw9bk1j46fwuXxDZBqF1wlLN6fkISfLEBRrkppYkSLT9WlRRFerqrvfzXK2zciJ3Vu9f2QKDTpoy_8URoEod02eSLYMbmg7a-FjHdRJrVZg"
REVIZTO_REFRESH_TOKEN = "def50200c7e21057e365829c5d6677a09ec6e693357ada251ca7448b664507ba52f5ae40d238e281939ec05f7e72a756f7dbc8673b883e9c692ba60bb5eb132a99eaf3887803ecfd85e514e22ab214f37b4b458f6403716621438fddd6021a1c9cd2f4fd11302c53b9a0c3d34bc8affc9e1cb287cef27c866cab59b53fedbff3087cd2a8dc3d1debc37bb0a8d123a432b55c6281b4fe024587c32ebf837bfa8772a46d2d28daba6ce7b8f1ba9df6bea951ac18d0d370b11353ff37bf1f4bec8c2f98650444c8329208e65de30c2fcadb7954f7c8cae180e6943798dde0cb21a2d8acce49a9c60c283f10ed42c5948dd4fd0bddc116a99bf9684cd31b0098eb17f3898b8060eaef0da52b4bd5bd867d7de6043dd2e0ad93c5da831ab9684188ad3c7bc75bbf5106904efe41dbdfcb0894865a8231c9178d9f20a5a721e2b29ad6d833579bbd4f91efba96baff1121c5e01a47c83288d043cd70936b75cdd583d96a22f86829e25317d9ee6f2b58c89170d34ad3dae79b834619ccc7284c2b1879eb393d736f088f30a6240463c8ff44ce341928605e66315f6f74998fdc9b4988e54881028fd258df7206c0e51472a9ff158d5c75f2b348dba6a27b63fd5990ec1ea0f12739ecd67951bf84e32b1859e03f2e30f6b75d39de120f234661f147f3a37784df22756f306ca8f2614da3cacd957c443d4d4fa3802b7fa75a7a4b661198875474558490021298a6bb1205260355a762365f54d69b40fcd43f0d4c635b6c8e21b43c753f647257bd56e3d827a44de7f01b43e08d5b714d3b77cee9dddf2599183535d31f9114f7c51655d97092e945f73191a60d435249a949"
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