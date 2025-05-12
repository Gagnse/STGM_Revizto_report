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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6IjA3NzI2MDE0MjllMjhjZWRjMThlYTdjMzZhNTk3ZDFiZWFmMDJhOTZhNjk3MTEzNzU1OTg2MzMzNDU3MWE3Yzc1M2YzOGQxZTE0NjJhZmFhIiwiaWF0IjoxNzQ3MDYxNDU3LjAzODI2NCwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcwNjE0NTcuMDM4MjcsImV4cCI6MTc0NzA2NTA1Ni45ODUzOTEsInN1YiI6InNnYWdub25Ac3RnbS5uZXQiLCJzY29wZXMiOlsib3BlbkFwaSJdfQ.M6rp27_6myRrJ_Kshk4as_guqzPlH9lpFzEaOtwu40ux3j6D89vqQhju-nZ-VcuvZMk9jSAnon3XS6vIThcmepJiOgcS9VTGkZzqUW92OkRZRGLLRHwRGLEkBkVSGy83SEXhHm8jPoPgsUUrnUXfQ23vgorsQFrMNE7AGMLlEtrU_g5XshZNso__ZwBevRctukId32Uwtbdj1Pcpsgilki_n5SfC5Za-59RcA6Ky8qV7E0aaCQ4rtb2VCeglh0PTBISAhmbb_DzGyjBdmSO_EPNvvB_rQla4wgs4KXmJPr_SkwtGnlrqySKJpjMGQxnVM0PRAehlftIxfpCI-I577Q"
REVIZTO_REFRESH_TOKEN = "def50200295cd65cccf76ad72f9b42ea9508111cdbe23f4db1db66d18b5d4b3cde950cb55fbbaeef1c73aa8af5101198214c7c2e8a3314e425e277d8183319572b7102d8445e1b994bbdea590adc6bfbc6e06477ed25b712542f5f9e70e8a7f0bc412620f424d1d86dc95719ae4b9b10cd464c1c249b0fe64ef8db5eedd5f068507e1265eb7d1f594fed6b0b0a05f5871119b3abafcfe781774ff3647a8532209fd866a12cc7f07808ff1dcbc351d5144249b6cd32bd8d4f83d22d935e845c25b2bf9d0b48caf83e9eafed6614e126fa58898bd8afff3037bd4f4cbd1b7da809f8851c744624d996738f48f1664b685425c82eab9abcc0c2bd8ae98997036922d9876d1c30bd577227911923582f4d2645bbcd86d088e0904a256cd97e6290409d84ddddbeab6eee5475551d9f66518f99ea4c3303ec30e4920da3a38ae7018787b1601a4bf27bc474296561a3146bedd8e53cd3cc78aeae9657c102ced6ebd1c755aec2130a9208ae9407633a5d906cd349bca58a2ff000bc0d7482efc59879dc2fac9b4667c24fa43db83b26295e8b78a1c4b910ebb237fa01fffd0413d742877388d665cd96045ffd6efdc8cf1b09c28bf1439d885199f1891b030b18512d01114b9cb69149a783fb72bfc4ec139157fc0371463bcfa486e6cc2dffa6e4915a67aa89641cd84e06c8d7ccc1183bfab701029752e4a9cd7467079cf79e0294d13d0a483235c066d2932f711a60c0d75a30d9ebb0e3660e108ee571c5cf243b0c1797a2464203afd2e9c544f124a17468420bda3b8658e447e8fa6f30cd550e5da9592a6b4e9b4697e978fe84fa3dde7716bdbb40ff15bc3726798e"
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