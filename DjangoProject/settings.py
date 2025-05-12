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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6IjBlZGRhZTJmMWFkODkxN2U4MzEwZTE0ZjhmODAyZmQxNDNiZWRkNGM3ZTllYTI0NDljOGYxMzJhMmIwY2Y3OTcxZGUxMjgxZTg5OTMzOGUwIiwiaWF0IjoxNzQ3MDU2NjEyLjIwNzAzMSwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcwNTY2MTIuMjA3MDM2LCJleHAiOjE3NDcwNjAyMTIuMTU1MDI0LCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.F1GSTYZ86nALHwKf8KNVzIlFoUzDg7iop1nUXdW1yiYIt-QrkqDS6g6iISp5N8PEZEEeix4SFOzXdh0PGn0T2Z3yr4VpiA-iy1C3K_DAHQBguiDPrbkyrNEHGdubvkkFqD_NpTHh1u9fQElJz6ZIB9Ke6ELXu0tWjfP5ujZjJydMVRgDO2p_HZ29BGxWMSPA0eylSoNXWPznXYiykWuCcQKKJxT-CST1NFAHRATf9gsgC47RWpAlfI-8aIoJ-1wOgmozZixHSpivyckyBcztlSsEiBgM9Q4PX6yG7ybxO-1C2C-xhCrLSN8zEIcS-VTONdWZNDNFtGyNA2xMpS--vw"
REVIZTO_REFRESH_TOKEN = "def50200b936cfe02fe53eeaa87b57bc5596a00d885a492c8191c5d3e5eb3866c7ede7b83e9c2628e78f784e07acb996906f49d02d27fd5763772d4a98a89c7be428541f9862147da0bf89b95c1198e63138bf63e93e01a3bd66f9bfd2bd12c634b02fdd3032d24b2c51f16237777d63800f260e9d497fb4e80278e40e815ff4eeaec3e7c0f47bd642a8d0eb73bd612349f9aaca128afa703209402780c210663bf837ef0c569d39ae5660fec37ea16b4f16ab1597eec398b201675f474b6d77f3c18c4a7f236b44d48f0db75d1aa9af219f181134ff0e51ddcaacb197a6a7f45dafe977d36a50bf433f4295e7a94ad2ae4eb7b5d240a52565a23d376a3f78617f2553b440b582c14b2dcf000e61575094146c624c319adbff408dde4281156f29470e2b27b15b3ac57c62891bea8c6f0cc3704cb60af50284d99918c66314f8449264fe47c71b3df4a23cc3e1b90016b39ecaee60e5c57339e320c7a141d59dbd85a44afb39782564e051bd537dfe9a29c836c763ff7b9b4c910841ad985b8f2e81e2d80c868c8454c7214f3f807897d17c3ae34b03fe36544f6b1d5a6f18dfa8a6b04322e10fcd762f5f87626315a46ed0ddb8dfee2fcefe8859388d49a63ab809f32b14efaa0fad37030435de89aabc42b84d47e7a00bfa0ce1b972a220e5819b33ee09137c790a218ad55ad04611612913f7859e2d2820c7f8488e3d6b7a552647d6d15de130b7617c83df9ec3fe92dc345095f0ca1174cc639859ceaa842d4aea610268c8cd1a6d19e320e512c201c47729c02980b57e47bdb2e367fb39849b0776a276fd3563b9960de44f24c832675d18609de3f9b3292b0d"
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