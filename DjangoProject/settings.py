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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6IjBiYjYyMDliNWQxOGE1YWRmNTI5ZGE0Yjk1MmRlMWI0NGEyNmQ3ZTE0Mjg0ZjdmNzE5M2IwNzQ3NDYwZDBhY2RmZTE1Y2U1ZWEwNzY4NWE4IiwiaWF0IjoxNzQ2NzI2ODU5LjIyNTgyOSwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDY3MjY4NTkuMjI1ODM0LCJleHAiOjE3NDY3MzA0NTkuMTcwNTA3LCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.Or7oBKH5q-CVPybLft2pK2dYrBj4XtgNeVLQ6RH2Ledy7x3jiX1U3gNZKaiOQ5sHTo2YXG4vs-k7c69Cj4B9kddazLXpJAmVfNvv6Jwnm4Pkn21LFbedWdYfwHzEa9kud3kprCmVMPSF0XL_-UJxvfUe1dTvi99EeLzCdeg6y17Pss6O8kI3ru6sU710-Os6ne8UmmmWuwzArdVNuy0trfjipYtKRtY5K7Q6gUmJe1Sn74fuCf6kZ5Eg76zu-ROosl6ueLb4V4GZb-fghaqc0bSnpHlsmfIudEWeoGjRkQGBfSsg4FPEMUWkY5aweoSmrGH1RDD-6mu36w8p-gZIkA"
REVIZTO_REFRESH_TOKEN = "def502003ebbc0078e806107c05b3c8bbe07ad7b320bca055670d280085cd64b745a038896ff5658216fbaf4c4900556e481eedc56c0c9b39bc070e28f00fcfa40fabe753782fef40c0d2829d636d5f6c2cbe37f4704ab9470934ee5993327016639c981cfafa9d65d7b494dd97cae9a2e96ef4aa0f18599995ddb75acca46daca2f054051f524abb65c954e556afd4b2a847c099114dac2a1ff053062b7d9d79e2c639444c9c653eb6c16d9ae7614820f402997a21da576706b39201b3a9858a57fd7e472ec350bce8f1e33755d5bcc17b52ea7027b528192d1cd253d3bc1aaebe6c02c4c9dbacbf26168502ac0ec50dacd262231add1b18d8f2fbe8baa6afc20853b2c2b1516e2908a5563a47f361a22536b69027bdd7e6176cb91ff420f03ee4384a9d7c219362e9bd22edde9d2861350eba5bf376b6c1b349d30ceab935a36fe6585109b3b60ac6972228cb27ba9129182219cad66d9eca10a80eb6ea6a585088dee2aa4e8cdda691ab6f20a6dd5ec6393e4bf693084da7f5ff2f19b474646edc12e88c9c8754c5ba060b0db557727ffc806061849ff4c78021a7b86e5e75d8b4789e2b747044c3f330d157b7d179f12db45a8c0b16f427df5e9edff02154412632c9af808af48875216484d1d4421c5684803774706b3dbdf4322c21c25073b089f14b4c5305c4e9f10500fd9e49204fcd5b724b83c95dd4a1feeea43db60cd876c19033d8c73443a17def7e9f0b35c9c87c314de55af6ae92ec50500e155f05d00e2f1916070e1697267d04573a293c84904e49efc09fa72fb5f71c7ec83c26930de72d8bec2d2ee4a051cefd943ec416a97164ff0ca340ac6"
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