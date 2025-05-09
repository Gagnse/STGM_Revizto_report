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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6IjU4YjkyMGQyYmVjZjliYmYzZjI2NjhjYzE2NzJjY2JiZDVjMjQ1ZjZkZjdhMWE2MWVlMWJjZGY0YWI4Yjg5ZDUwZmJlMTkzZTQwM2UwYzRkIiwiaWF0IjoxNzQ2ODA2MTMwLjU2MDEwMSwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDY4MDYxMzAuNTYwMTA3LCJleHAiOjE3NDY4MDk3MzAuNTE4MzQ3LCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.rnx5mWoBswgAhpeuW7oi4J0sUjdPLLEk4P5WdCwDVfJuY9p9uWWEgQ_KluRHw1AguLTb6Sx2TBLhYrFZ7eoRp8vZPXao3ldcrxuD2AuHsa7dl9Di3Nkr-wqwbdN3qm9qLAWD5B1mWh-xRBAWlg8ZSncsjixvOuwNuL5HcI1aBy5VZnZCiMUjEY1vbDi9USTuivcMhhmLN3oaW-gQzMDVC568iq_AGtztBPVt-6juKoaw8bOHQeVHYCUjP9rEQMzWUod2yzhqIUM0tlyeerM8-tpqKekAlcyaDh48p25BH2OkOHzTxShHVoL7v0Ut7lwesWM2p2mrIhClwhSZWEy_tA"
REVIZTO_REFRESH_TOKEN = "def50200f9703a51655fbc8d4a0aeb1abd99129459ffe466f620aadaaf4c00959ed7b63e8cec251ef13af29517f7d18942e3f1f24feb8391515962fd58c797d6d8b326a16f5ae453462251c1c220f74efb9090862f4debb9ac33ac5c042e1f8b63a8f44b1a828df170b11e41153023e3aaf7ed31ce7b4515be6267496e9fe1043b662733b1d53b3658845979003ed2ca99cdee042ceddd9853ed88cdfaad6a3ccb9fbdfde09fdda910259aac325c0e6f9fbcb92e0af4603d31962e4d96992d0aba3e37d215633d2823b09424f6656a428caf479c894b96b2090907c9c57e7e12f441997b1d0b105dd3dbdf338436594e6efc394b31ec000a6f42f6087dc819d6da8a02dd9fb738664d592221d8d95ba06f4b9566290494b02315a0d408e935bb6623ebd7ae4b6fa1d46ce1a4af254bf95b8941adba462b7787ecf7c758e76f49c60c0ddc23e5451bf31a357cf31ed4e40a95f2b9752487206659b06ea630ca78bb02341efbe4596970e8b589514f78b7a60288359d7287def862ecea021a3c03f83a44aab0cff3c7799d869de2d364c174247a4fff25a7eb47fa8d6fcf221acf8eb33b245d70d6cb137969b0535ccc0ba2a0eb5a57fede4c9aa0f283021a2c0d7ed48871eebd93df342716987feac225f34a71d54e52c097251b6cd33e2c0ff8e4e142e676e87422173ab7aae924cde442278265e8e0e4eaafb9dc6495cfeb47c29f0edbae8e05905956e039a70d913f6574485610d9421e58745dea7d91c5ac07f3ffaa6d14086fbcf8885535c60e491954dc39d8f23c7ba1d7e615fd33675a55553b248b458746f09365e3314db7e4a059f61503947bbf340a0606"
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