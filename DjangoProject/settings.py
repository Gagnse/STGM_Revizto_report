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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6ImNjOWE1YWM0NGYxZmNlN2MwNzNmYTYxNzA4NTc3NDU5YWQxNmIzNGJiY2RjMTA3NjJjNWVkMjRiYTIwNWJhYjRjM2YwNmUzOGM1MGM2NTY4IiwiaWF0IjoxNzQ3MTQ1Njg5Ljc1OTU4NiwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcxNDU2ODkuNzU5NTksImV4cCI6MTc0NzE0OTI4OS43MDczODUsInN1YiI6InNnYWdub25Ac3RnbS5uZXQiLCJzY29wZXMiOlsib3BlbkFwaSJdfQ.cwwS7aUgkRhlKUzblPb03eSqQS8bwWx5ovjvpXtWnjsV0oeoOcAU-SBiWSxhN4qjNJ_XjoOTSa8DzBmAIIFcp07eMrFaRaa4hYyjPS3VV_5iKjJMQ9DivwCjKKzcIvFB6CRTzTJCc2TQCOUUm7Kmk8MLOLHaWIliIy8td3xcDZsDQtt5vt41uj2sfvB_9kpzMIYpGIcjELRccvdR869xGIJZRjgFnOgPpP0PVBlkmx-wsbIkOp5QDGhH1d6trRnCTUpS73n7MVsJjgzp2r6_PG1dTaXn_eJyDmdKc5_vHm73MoeQt-97LwL6QbQkGdtXkAffs3ds5TcdmCPtGajIaA"
REVIZTO_REFRESH_TOKEN = "def50200faa5da9a17b6f0d865b6e96eae3f42e9db33227681d725285e8e4bc88d32f9f80987cd47130e90029bb16e27f79b3afef2c5e5046a9917624157f3872933a2f9454c1ecaabcb87f9fd53b617a4541405d84d5021f3a8d887ee6b392b345783afbd92bb66bab76f417c2b3cbd39de95ca0587679a43c30d4cedd64b8461ea9a0da810794420b1301f2a31a1614e427070eca34ea9e8269095213677b259bc6a64cc5d9781eee751552d34fe9c341c12c4b4d8d243120448452e945fa5351ae93665e95fa8ef47e14e4554f5cff00afc2ffc0f53cf7954a681d183e086a18cec8d472a4ba88d55fb17d3458bdf8c0f7cb157768040119ae6737cec0cf4f496bf86c1ab671bdf6786dc9d526c3a128cc0f0b764a62c74165ee67a41f98366723b84564b43d2650168dff805ceae3bb67882038701acfefd9a3fa09c3ad0db078d50ae3bde267d0241183d08747c9cad07c789fe7d5f853cc3489a9352c25c589dd67d944ba605ec2bad3554878017e591844d0b8169976d927f21437eb7efd974f73c524f7d5bc9519a23a962ef3d42c8ff59c5b34d7210e06a12ba6f93879241b82eb41d3fdb6ef188ece105b6a6eb13eed4cd6935cad798f8dabc27611d5191cc9e8d5a58b5d87fe16b73fc85c1fd409372a3236c386a51347a315495acac956473aeeadb0ecf547ce349838ab6e5aced4c52df15d879c3b38bd457347e247bf3cfd22959023937fb7fcc972aee46a1fd9ff5f3a825bf9d18f046dcadee02533cc95e5b9f4e737df89ecc54f6c690bc3aaafa47b3e29444ddb184e06a5053310e724467affd8f8d8fa4c0463ff5d9bfed0a02a8e0b7c702b4"
REVIZTO_LICENCE_UUID = "2e38d742-c9ad-4d11-b5a8-c9b53e9bf517"
# For production, use environment variables instead
# import os
# REVIZTO_ACCESS_TOKEN = os.environ.get("REVIZTO_ACCESS_TOKEN")
# REVIZTO_REFRESH_TOKEN = os.environ.get("REVIZTO_REFRESH_TOKEN")

REVIZTO_ENABLE_TOKEN_REFRESH = False # Set to False to disable during developmen

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