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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6ImIzYzE0ZWIyMGQyY2JkZTMyYWU0NGUzZDc2OTQ2YTk1YzY4ZGI4Mzk4NDQyZDgwYjQ2ZWU5MDdjNGI5MTIxNThiYzRlMmE4ZjRiYjlmM2M5IiwiaWF0IjoxNzQ2NzEzMjY5Ljc4ODA5MiwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDY3MTMyNjkuNzg4MDk5LCJleHAiOjE3NDY3MTY4NjkuNzM3ODc4LCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.EK6hSHV0LK5OzaNStfSSxVYlB98ypOyLaeRpj7zrfEXoiZpuIiQ8YbwzFTPFe-LOw330m4QJelJ5_6t-XHGymi9qJDXKP84moxceIVuu6C0mUmpZA-w9ZoPpNvVsn-MF4GWcDSFV0l4Lnzx5P4sKpqXyYIQ3aK2LNop77pegDAQB1HUANhK4HBDVU9vK9n_-qbrQuCVzygA__oCS0nxap300vxYffz5hR5zbJltMLtYA0-a_EBhtfw6dniPW2YcKH4Ds9rOvIk8GX3SWzXTDP5Ub_Yrue31G2M6ztI1SgcyrARcDYuBFVkqVMnEDqn5xyCq_I32XMmL9ZA9obeqM5g"
REVIZTO_REFRESH_TOKEN = "def50200dbb44f04f9050ad94a90dacd877d71dd5db92dd26a00460bfd92462c923114fb62dadb13a42501ee4e957b36c5d13362308a5aa46afb1f51623bc88e19f0be25cb7430d9d88f91c1a351a6c672dc3fbc9ebb83042f710e39750fcab9e65e376e8e0ce0c4b8f8866de61579f502c867cd0d731f273b0baeec3bff87f4bbdf40ad65c8f232e374d15ea0102a87762a44d60a208fdc5bd6e5d320f12a7db89d4517536b7f817a8c7bc666b73069bde956b035b31d5fbd3204655e242cef50ea4cf108c13d30255ddb0ef9abfba0b73be0d0e63c5630578e4853ffb277f7ce8ade8bc80bbed418c7bcbdb79b044feb16d976cd6f44c938c1ef2275a2edcb87a9f50d60545acca618b4612f81bed446d80bb23345ff3144a7bb3ebce73d92603df7e15c0670c9b98ab530ce16006065854e7d55af8cf5ebb0784025b4eb5737a70d355fd991440a3b69753beef6d88a62be20fd8e61f049b710cb97ae23231e12e0eb7c2ca80b35af3413699e8cb5f0095fe36a249d2f7ec8df33ccf4829c7c3933f74026e77fa864a507c20239b2e9ecc26ce46bb06cfc8369ed6f0397075970e74ef38df69173bfefa4f501a5f1ce4b263ad094b2c2437c70b221760e324c6aae21ac4b5b5f6d1ebfd84cf8630f86acb7976bd827d928f44ed6e3f17ad1e8290554280305d0ab0f65357e3c71799beadfc6a529f2a60cf4ea8cfb70189ea8b35daeb7a9b66f2def8b4e83e10427a8e53055c2800d16ca0785a52d98b61a3cde96f171211cb92a60d901d92f1825bfe01ce8cbc60c7b5cff15e5f3171705632c73bc0f5cccbe21f965fe8a5416c2997bca37f621d22edaa4aa3b"
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