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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6ImJkNGE0YWNlZGJlMWM0NmZkZjM4MWYxMDVjMzZjNmIwMWJhMzkzMmVlZDgxNzhkZmJkMjU5NjU4YTJmZTE1ZTJmM2IyNmU1OTcxOTFmNWQ1IiwiaWF0IjoxNzQ3MDc4Mzc4LjQ3ODQ5NSwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcwNzgzNzguNDc4NSwiZXhwIjoxNzQ3MDgxOTc4LjQxNTU2Mywic3ViIjoic2dhZ25vbkBzdGdtLm5ldCIsInNjb3BlcyI6WyJvcGVuQXBpIl19.ny7C54aDJOhZ965xOace51wJEEVcuLu3EeYpo_-60-_CuQvLnexJo95H3LruuB2vOeligBJ3xrRu9hlAgw9J8BPjxy_FEQW1sq8Tcl3-AQepIG_UhaH9hChGFWjHFlj4sKHCLfm3DE_RMKAXI-pu5Qlu6apAS3-jOuidyo9wFKD0SP5i0JP8fH6R2OXDBs9wehInC-4QqkSLMhy6Ln42akp4J9S81PuopBWIwo50gph8CElOyZL1Q_QAz4KSldBUQ9nvAOHvCnfnHZSPBCGjhzkscIrv_fUvamivCTh6pqgyGRKSnAlJtOR9r5zunIG0yqqZl9IT4nNc2qg_yMT1ig"
REVIZTO_REFRESH_TOKEN = "def5020035976d0bcd71f6fe8c22cb8d3e37d8243a8a0a0b8e9446d39ca7ee2e2d53b1eef2ac67b15b0b837ec490ae47f4e0772acd12b2f2048fddcb2bb9071412bbf37b151aca192fc33eb259470d6e6a68f7088391febe8c9e490146208889b23d0bc857c08c43887acc24340abbba5e47cbf31dad6e28316d26d31f0cfe7ca2bfb420295672d2823e031ec052c6fa54699ef70f4778213ca8078da59200f970924db1acd194838b6c90f10a86cee48a62066ed6af4833cd9630311c221655b059648ae5bc3b78ef249388f7ce07d19e6069d3cdf7fb29c54b6b4ecb27ccd9d1ea3ea5f604ed66f421f5404ae40efa3699f782385bb0dccc864fc6276aee614196ad061560811fa08da68c284b843656f16cef3b35d992be89b66c2cb5a6691e39d27c1ca0119e677384c897f53e39b3c966e44e8d8c62607bcb2477f4ae9c99c5290a8982cf06ff976e7acddc9880cb3fcb4d039dc62d71de610340d447eb3f1b623a32c23a44d7510371d404dc35e34a30c5fcc0f2e270f36ea71126c9b8be5a4b556f3c421204b29923ebb6f2b53b8536f1021b0869a61db1a7038b4e1c6df60f3502b338b259b55ff5b0ced0d1a50941bb7354606e252e2c084032ada47940673453f3016957235c277ec6621ea0279702791c15068fe5238c58841eb7b6b3007c4683c79cd0bcab0ac58ffe2c4d065eb27a1317bd4dead78a5dbddeff96ce57b07968c7a93e9edf5d5278adc93f783d510e9677a8e3f856c423b95c2139e40742ab0b9bb3c1e7d0850e8c8615427bbe6b55916b9f09cde59573749939f4a2f4712d492ec594557b4dc9a497a44b90f3f0a15ba5fdc7ab1ade"
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