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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6ImNhYmJmOGE0N2RjNGIyZDliZTM4Mzg2ZGY0NmZlZDJkNTdjY2JmNDUwZmMxODBhMzJmZTc0NDBkZDQ0Yzk2MGY0YWI3OGVhMTQ0YzViZWI0IiwiaWF0IjoxNzQ3MDc2ODY0Ljg1OTM2NCwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcwNzY4NjQuODU5MzY5LCJleHAiOjE3NDcwODA0NjQuODA5MjUxLCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.IhiLETJs3MJo6vLR4UHA3xY4CA4RhXrPIE-DGT6wvsrTgDC_YCOTixyrI3peTaCvp0ON-p7G5SXUZK-s9TNqY0yKGd21hKIntatn_hRwH7nqpv5ow-lhRYgppUWDo7KU1oKuKZNtavVJAckLTb87RpWA_6qWKMetUf9_iCljf2Ms7Vyhf8MP8y6SI5hqaPb3mPOEQoV0kMLVYHrCKtA_X2A7XlV0qRdCjXoNSGk9F4xIYmevTrQ9qxQOb4C4DcYxv7lBdPUSMBjIIYH87Y6xx1RAtbvv63E72_Y3ABMElCx1oOf511sLCPDbtItaxYe9RJGByd72zoVUKiuGCpQd2w"
REVIZTO_REFRESH_TOKEN = "def50200be349dec03c043bbba4e32c9c5333a143d48574799fe9adf01393d6149402b694b7ee50c0a348ca00175649bc976ddb6bbf0e8c820b3ca0543a7759396f0a9233f5bb65182a28d5f78e004e45e45eec087cf2c1f9d35e1627f243461b746de8c7eb254c389a1d873c39584299a2b3fcb27fba3f4641d5cefa470c17a6ee874509e8b33f8975bfd5ef1902ab2b121f9a467522726ccf328fbd49ae2d68f383cd4efc97e446169fc87cb9ca4f9b24eee48d9fdda1ea9c643b7d5c5e7ea0059129013d0a765ee4f6ea22d3fb3b2be971520ec1d53f3d92096d35897ffa01a8717b3ba1c6c19bc4db4ea978dd1f24153f011bb6811d2257fa2524816b97eae0b89ceeb832ade7eb2ee1fb156d119d085f2a1ba40d89676d51bf679f9524464284e8d00a83344435a22ad4e1b76497dc5c92f1f3f9f4dca792df3a875487309efd021e78c01260dafcc33ec5119626077942f561aa1b41252277b55ff6f1b0e21088a3b38d8da2a18075b34c45e842a5ecacfc9460bedb3691da10557e4c534c4858eef6521c60dd062f54f076d5700f27147f97ef2032815932729ed7ee028428201e5cbcb95e1946a6d46a07bc0190b666d9154ae4d1009c5ed80e4bdea1533a7c89f38779d9e14fd5699d5ee6173443ad299f61fe0d717c69613b9b1969c674d3fa9c8557da70c99cc3b1d32f4ba3fb5fed2811e98630d66f1f4a0eec61679bcb7d5292ef18024484c94b242317befdf59876dbdc0007953fb457bc19d640c22d73ae14cf3a99a71a20add3ae42fbf75af9e59cadabb6037622e999751c906198091117896fc143221f0b3e60fedc138625f4833d30f6b7e2c"
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