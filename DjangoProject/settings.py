"""
Django settings for DjangoProject project.
"""

from pathlib import Path
import os
import dj_database_url

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
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

db_from_env = dj_database_url.config(conn_max_age=600)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd4qfmqaelhaou',
        'USER': 'ue3edpfcrvn1iu',
        'PASSWORD': 'p927ab6c7ca5f443100468557f9683b9b94ab0cfde3b745a42832502f43672c9e',
        'HOST': 'c5hilnj7pn10vb.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # This points to your static files directory
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Revizto API Settings
REVIZTO_API_BASE_URL = "https://api.canada.revizto.com/v5/"

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.herokuapp.com']

# These should be set in your environment variables for security
# You will need to provide these values
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6IjczOWE5MThmMjQwMTY1YTYxYWVlNTRkYTdkODVkZGY4MDJmOTdkY2NjZDJkNDljODgyYWY0ZjRjMzcwYWI1NDBmYTU4NjQxNDlhMzRkYmI1IiwiaWF0IjoxNzQ3MjM0ODA1Ljg3MjMwOCwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcyMzQ4MDUuODcyMzEzLCJleHAiOjE3NDcyMzg0MDUuODE4MDQ1LCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.l_xq26TJ0SYQa6OitTYpi1xJK4SZ9w1T1sf3OMTiDBFgYhPSZvRCbGRxbamR1_WgOw_kSVqWoPRKk6u4LuLwBxYNx6XKRwteZWbZba9PHBzzyFwybqKNef7IW6p5gb4fY2m6N8LbcOQKhHHSyPVTqUTmD56HjmVqtEtwJGHRBjQbixKAfV0SP3GZNgc1uyRG_kBSA7UbOOIOphO8C4XqnLNj3G5H3ozszVRgUek-EQDyCuNzfRMtcREpienDbX4ALiXE3aOyU5aFEwCILT-E62DJ_4pw07aQVTsGcf2EEvFzYCE89eNg21-bRldWaBMTisGjaBjC0B6Bx-lGFzNwBg"
REVIZTO_REFRESH_TOKEN = "def502003eb60220fe24b817ad754c350fd2cb4745814b79717e86bea216ce0d3f4dbd43b8204f8ea8116aa042263cbb46e35df5ed41bdd148d656d5eab601f195ff1d5d178c6dd7e7321c9566cc5bb528c47218b07637012ed3c5aa4e5f48676ed5aaa4b4d46b1723c3bcc16c0cdd6684a7fe26134d3098e10e4084dd548532fe3684dc61dc19d3c700c5157bf5bca3670844b323ee39b1539ab34a991f5208135709543b3306075d8ae76e3561c1c13e326e3a9225c1d18f0c5eddbc29367f206b14efddcbf8cfd31f841cc675c7c0943756f6629ced10ae585d7c659b43be02ccb21ceb0bb0b8daa635ddffdbdef7786992fff4760df893cabf414e9785a6b82683c6871dfddc5f076e085bbeea692a180e7ab8156e9066a59a24e602714b4887e5a78d97f2bf6cd23ec93538ed126ffabc3ea9c99b805dc3a3641734f9ec05a54d34b98842e8c828607247916ed0a31759e569da9e552d7f3b8c68e68cd24968b6c658cb23656bbd5f05783d6845c59abf3f3efb0421d6334d1b190576469c262994a8c34dc98af0e039336a9ef2a13ed094d133ada149420f25bdf1e8028b6142fa603d17ca7b60c7765f912d8087ba0faf2958cd68bc441bc78180597ed16a63f35c9a1d8b07369901656fdb16f57a86081681a4cba4eabdf4409a46328d18df8a59504a74ece8e95c076dab20c558b35ee13f0674932fdb946008b4f7d32e31e0295d1eec6dfd1bb8f4226439f17d54ca26b1c49e26ad877579027bb156e96d6238ce962ffbf6c3a2152fac7841c43fe38d3c3af4ea07e90ac67765d5619bfb8ae5a49756474250c3095353b99500a351b392c50094eea8f5"
REVIZTO_LICENCE_UUID = "2e38d742-c9ad-4d11-b5a8-c9b53e9bf517"
# For production, use environment variables instead
# import os
# REVIZTO_ACCESS_TOKEN = os.environ.get("REVIZTO_ACCESS_TOKEN")
# REVIZTO_REFRESH_TOKEN = os.environ.get("REVIZTO_REFRESH_TOKEN")

REVIZTO_ENABLE_TOKEN_REFRESH = True # Set to False to disable during developmen

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