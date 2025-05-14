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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6IjQ3ZWE3NTBiOTg0M2ZkZWFmYjVlMzlkYzQ0ODU0Mzk2Y2RhODNkMjM1ODE3M2UzYWZiNWQ4ZDNiOTIyZmFkNWUwMjE0OGY2OGFiMjBjMWY1IiwiaWF0IjoxNzQ3MjI2NDA2LjQ4OTk0OCwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcyMjY0MDYuNDg5OTUzLCJleHAiOjE3NDcyMzAwMDYuNDI0NTc0LCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.oQepT09A4dOQG5BWyfJYGNN54LzAjeEiS2d5K1uNOD9JcuLIUVxpE8J0BAbMEMEhDZOidW8xE3eYbF_As6BGZLRgW6PhMBmNB11mSKkPmZqvrQQJZzbFJxafqxZkx7E7Nm6ONk5juTS8Vdi5Gt_-wz9jSy931sTLA4NvjF8n9q1nt_AUEjPfcqF4pAxtO-yde9W7MJeCfHz7EJBOC5KvIbfmDmDD8P9-l13k1sHeW_xgZQLd12Xm9sMTeYXpW0qmPDkQXtdTLNiYXuM4Zyjvpbv2GqleM3ZbOULHt4w7FWo2JDCvNAw-GXXqYPqLr9963dYpAGZFU-QdH3biTyaYQQ"
REVIZTO_REFRESH_TOKEN = "def5020099c7eb6bee27e1f193736b0cd73a02cfa40319e8729e7ed3ac082efc5d3c345b61bf9b5693856b6414ca5b0224f2c354563c86aa01cb9768fb8ba5c41d9aef99f1cd32f5428c8d624d9a50b13e521d81665ddb0b9cb99dd3e24572120a3f3f246b45e00dd543151798b1d4fa9ca97f3750dbef74c3f72087b46a55e3c829fba4630380f90900087693950dd304f6c089c6a73adfe28d9bebf8631118193ccaf7ba6ac39b6e09643d98bc336986d3e35d0e0015789f1a9713d5d5adab49a0e1b4f1d1e7e4de62b02c30a47e46b9d0a65bc4a0531446388eaf145acd300c8710b42264b92f63257819af3dc31fa776779fbaddeae7432edc4d7689b22037ead82dc77f9da5d0fc7cc4c70e72754e51e2e7a3f0bdd65d2a48928ce6fa65c7a2ca2007ce55a18e06ad3406dbdc385cf9107bbb27978ec95ad2ebfeca41f99b412685fb917737dc7ec8215e7a07dd42a879b0321986d303e1248baeeddd4bf7b98083f6423ba2093bc0774d58f94f2d139f4f42141e071f5ddfb6da3a92502e263d4e631fadf8feac53040b24439ea400278e4d51d39b2061e0b02527bc084f6852b278ebffee239920ee87f26a16580ac3a34c3896bbda94fa1eb73c1ae3de5954d08b7cdb0d94ad5c3a31551e00f9ed1139e31e66f443315679bc0fd748afcd683c75a9c5b2a88a752672d7f6a60ab179b9f7985d3b19f5a5d9846c59320fde59da51ca4f45f50957eaa484d2b76e649cace9ba2a4861bea0048288aec48f2412e89bb6ccf330a46bd2bfa017ccefce3502de53c9fb7910ae5977fb3732f82a67158978fcdc37886732848c3d8a92a3480ec070d6d1d0bea3c3"
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