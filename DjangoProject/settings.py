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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6ImQ4MmVhYmUxNmY3NmVkZjY2MWRhZmU0M2RiMmEwNDkzYmUzNzBjZDQwZDA4YTEyNjRkMmVkZWRjNjUzOTIyMGZmM2U2OWMwMzhiYTUyZjA4IiwiaWF0IjoxNzQ3MTQxNTg1LjgzNjQ5NCwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcxNDE1ODUuODM2NDk5LCJleHAiOjE3NDcxNDUxODUuNzY0OTE1LCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.KKDRCGN7upTVdrAcD-SlRNaxATYLGestcNvIUR9Q3ZT6Y9qKPc3oyKvRHEfyDQPq9Uk7v9dYYdAGOQhk9Wrsmq1MrLl6hyme_KE5lfeVgBqyqhzTeq3v9gG43lCN_O3oYBHIJuiN309_MLECojbbGJxB60Xygwo3VYTrb8fN9yv_EezJXAinnyn8oxQn7aCFBT9HGH3XOxR6_IJtOYUE1Wtmdoq-i24TtpDD1MmIYq-j7m2nXe-iZtqdt1HnPzARqJRtIdGZjVLglZi-Ub8xQPmL0cmO2gK-nU8vbkTBigywMvjimzvMgRUzcz6Z3IEuTF7eZC6OOPVq5EsNHjQkhA"
REVIZTO_REFRESH_TOKEN = "def50200bac4456eab246bf7e4b387fcddfaaefc197d35747e4e3fee77193e31b2e6d48a65e795c75cdef10b66c4baa0542589b105fa510c8a9e889bc76d7ae09f152edade05175444c5aaf8c717f8c3917825c1d388472b7c6fc476e0caf14f2df1e9f715141576d3e290e6115e14fb4c22525980cf5e42b7648da3e8fce7608bbe493f9f107b0438d43fd11d265e26dc42b7338064c5cb6c77b7b4ca63e6f6b60c27f851ab62c75576274aa7d6081895cab2b901eb81d95cc6278b9908537899d04e949c1afd5b533231d3c437995fbb13d9268db866f98aa508d220e55c5ee4c0d2463f3e7c1e7c5346d52955ed2d9457caf0b7ee3b6ffc9118a9fd726ca92cba1ed943e0e9fa024efffe26497c15b8717f5148e255e4d5f10b66212ac02b5b90735d42a380133a2d332a16593e8bf079f7f638b668bc8fd45f18750c52a0298a182de947c606a0479cb910fbdd3cbc4b39dade0b3648979a6134e6b66fefd6f340a50d8343fed940b5e169204f0979eed0253d5b820a5d6f20e2590ea4e685b821506b14f6e8d41c1d26b88727745a2ccebe375d5618b3f3b829b307d0a889df4422f892c4aae70a8cf0c743799e703d942243b4efdeeb2b07141e191ba11f2ae45a2679ef7be314952cbb62e7c2d05f07d31eee3699a1b9f752929a9a42519c3b44a631ae10b549d4d542cdeb191dd5983c193fd1f6fba558ef13f7440e80ecba05d7ef066ce236111843d9af4a9d3e82a03a021fe0a1e26681dbfe21db72cd57189a7e39a39b776411edf0d240ee1af795cb9b85ba2aa39e7af58d3c491273357b1a8f87ff293bc81d0bdaca758ab7ce1e75fc6394654eb5dd"
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