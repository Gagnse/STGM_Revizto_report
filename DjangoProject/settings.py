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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6ImIzNTU5ODQzNDk2ZmI4NzMxODAwYzYxZjlkM2I1ZTMwNDVlYjcwNDk5YTZhMjY5NDdmNzE1NTUwY2Q2MTg4MGNjMWQzNTMyMDBiODQ3ZDhiIiwiaWF0IjoxNzQ3MDc3NDUxLjMyNDg2NCwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcwNzc0NTEuMzI0ODcsImV4cCI6MTc0NzA4MTA1MS4yNzI0MDcsInN1YiI6InNnYWdub25Ac3RnbS5uZXQiLCJzY29wZXMiOlsib3BlbkFwaSJdfQ.Ugcc8LU5FSRQDzd19hIK1hqVgbXoe-qJW6hyRuZAhSWRgH_bWTx0jlH1VGEjoUhYgXcTagn1v2h6fkzOJDdlI4vwC5UrboNiLoLlltdq2tHuDvMAEYgXIXHkla09CJNMj-mozv3m0QbTPGNP1ZHcWejohj6JPxbvCvGzyLlv0xudfKjw6tBCfqRPOM3UHGwabinW03DfOdNsV1CJubF0xE7C4pgKDCLpnc4fxLjFZXwsxeH5fsAshSekCmUVxORV-kvsyYzaKCJt5-Sn0Q8T15vZYIkUrelCVzFM1X-0n6iUn6c0hWP5xKxWKL89-e_RguRh1GbtLvqMUewzMAOgRw"
REVIZTO_REFRESH_TOKEN = "def50200aac39ffef3209bfcafc8c8e25dce95d3f805d59f598ca007fe898e861c1bb76d404bdf23ac4d98884db0ddbcefc75e87900771eed04fe70649a966a9cb99a484db6ca24eed724f091a3a1d64e36534abd427d747bec820842056545960090b55daf7fcfd18b728469f56b42923b6d8d8f13707a9e2d13fd778f3765096196bdd1d1c36945cdd8206347424b64c284816179015bda10b9afdc3b7afb9b790807ed78dc6d394314316c4c073e154433fa7fa590ba0f8a0e7aa9470d7cc08e642346512a4f90b49bd1cbdb6562cd8b900499edf9eabc18236d779cfd5de2f05b0a1ff3d95b31b8a8b8c25f4c9a87e1e3a78b9c15948beb3fccd05d1dde37a726ffad6facda1305cef76d04aedf2decf0269d4636587eefd153f3e4066b326dd8d0be1f884176bb552d05d4bd0597b5bb782fa1ef55d58197cfde1d9563da6542d7fa78ce0c9edbed1d884d6718f25876b73d603b197fb279ba8d5a8b83f4b16221bf786beaa8316b88f83ef877f27c92926c1e08d696f5daaf6e45c033aaef69932347dfa88add3ee1554fd915ec4599dee5e3c09ad855b7e8857f3552a976ab775876addd56c04d7d0ff02b4959837c97dc38a7481acc5aa425979b6f4bea41e46583477c7609edf2c7b7df527b351fc25cf94dcf0bdc4e6fd3170bbf6050b0d644136ece6b1f9a5d3b86a8147e27789f755eaf8b0ecb770a46de654ddb64c5efb6677032ffe7fdb99d809a416964ceae44f10af3ea9322b72411bf6298adbd66597b74ffa4510b4993d524485c20bba69d7eded457c00c4acf4fae3840fa4271aa3b683b54a31b2491d54adba53b05fefdbc6c694d0119275"
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