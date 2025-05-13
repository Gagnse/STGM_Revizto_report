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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6IjM4OGI2Mzk5YjQ0ODFmZGNlMDRhNTk5YTFmMDQ4MzYzMzEwZWI4MTU0ZTYxNzNhN2YyYzIxY2VlM2Q1ZTk5ZTk3ZGQ1YzZmOTA0ZTk2NzQ1IiwiaWF0IjoxNzQ3MDc5NTYwLjY5MDcxMiwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcwNzk1NjAuNjkwNzE3LCJleHAiOjE3NDcwODMxNjAuNjM3NzM4LCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.PGft2cw9zCPg9SqsanVRm8iHkqlZIIjlEKvV_Tb82D-Th_Gu17OlV6XYVvARMDMdJkVrWhT0_Y9gEA-lmn89Tl5oWE461De2v4kXhJQjLnNIXsrCnFyZOXfLMb9VrKiTLGS07L84bHSy0s-SBjE76j1cSrlqY80eFtOyHPulgA-mfoDZuyzB9b2JIXPT6EpSmwsM8kDOAAzLuebp8_nT3-vGIl0-BQrGO89L9mPEArn64R7urz1XacP6najehAlxWbEzmSF5gaP65LSd4MnH-iKf9HLBiG0LKsctX2Zf9dPIlrOZ7X0WPDpcH1VKDxqUktRF6bgrCbKl-p7DiHyZXg"
REVIZTO_REFRESH_TOKEN = "def50200a26102d4de3ac2ddeaf48f21e0a3350008f91d8275d9bd25fa9a738701b1974f9c1c0aa4a2836afb2958240b462edc41f27b2558de4da854970fa396fcd5c32ebfa9124739573fc3b89149174eb414cb104dbb844f9e91fc7e700906c89409cfbc4c467a037d7fcb6878aa1f8f4f21350dfcb55ea31837c8ea626ab1f703f8c4cd9db7728e2b6573475d4a8f63152cb484cecaf04c767ed60b82c425d6576fb8a1c1b3b6fc66642ba0dd910088db5e8a13cf2f40908c7b86ec98006d2bddedace754d3f95d4e4b4d8abd91b6d3f8d67ff27a34b232b5d3cb699235c75f26c0d8150e298ebc8059e20c0b0061f9eb3bd4c5657eed6c3552976d0896e2e63d7d6e686e90671642424e6743c8710893952e8b2849099b53e1132bad217c6be28725fc2a417a218cf5e32278933a7bc8607d90240e5f96e19be68d0ff6c1268dcf7026a0009006160af7993e788a80c869b9ab69e6bc19b26c428626e0ca090bc90dc17bdc75bae7342959ff4a3c5eb709ff69027e121129c900e66bb40136ff5fe202d19b66876939bc876238cbfa606da7861d3347cb8b55e2bcd97b2f6e12b16198b740b772889604f0ff60d7a851a2bf8562aba7c8ea520a035ef9cfc95daf7e366533d6e0cdbe35a63648772af96789769fef9719ad8cc2b5dc0fab6425f7d0e169416ea132f47650928f0b11a18e6c88e9e16d6da1cc674de02356ab573ccbac87fd1b834cc7f4b989e7fb5d4a43d72d46ab514a5613d8b8d291ed1a87533c119694630224c25165bfa0a7fed9eab00185af23ea2ed60fe9e566e8a1fa2560705a056c3194c227e7b7ee7230ac054847409c7a388a405c"
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