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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6ImFhNDMwZTU1ZWE3NjY2ZmRlNDljZjc5YWVjNThmODA0N2IwMTBkM2M5OGY0MTQ0ZmIzOTg2MmEyOTFlNjIzZjBiOGRhYWMzNjRlZmUyMDJiIiwiaWF0IjoxNzQ3MDczMjU5LjExNDM2NCwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcwNzMyNTkuMTE0MzY4LCJleHAiOjE3NDcwNzY4NTkuMDY1MDMzLCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.r9fbNdSW9DJUlCF85WvXPF8PX_OVKLtyMap0kUXV-wYVY6KggGOFM8ZaJuD021spOsM9aPtMtkNO084gIalfcmq2Ad32kPBC-hFAdhieM8clcR-60Mdy7DerQRkU-5e65p9ro_c0A5QS1jHMtvjn64nXmMt6qklWrQD-i4cFHaymVAvZHdLXDwvZEoRzatwyQnDhblP3yG8PriK9VXusCF2K7DdvcFNqGCLIghAjk5ogTMeoALLKUcFf4wd1pBMrYpJ8eAxxWNg1sEFFpuLYBkcR9uYksaBldH0p0RiA-7imxhN81gteNS0hnP541l7x4fxc6q19LGyvWB0pfdcpoQ"
REVIZTO_REFRESH_TOKEN = "def5020009077e57400a0408eb7063206bc6d39a308ebfa74e483129a05a4f31b76c28a655f4c010663d161ae769c3c69482477fcc93d6b8f04f27022d08eb01e4ddce4b5cd432ad6741e696a2c3e506fc4bbeab551c22e3510eda9c9bcbca4b43a02f265947f1600093e0c7624a77141842d04dbbc9e2e8425a096dbb3b2d7e60c05c78024130e2312a8033ab07285815910cc2d0b156b448ddfc83e554f7b34a1b00343490fedf0ca56892d5c9c3e7d32bf8dcadeca3901e7ba2dc3d3e9424d01c37d9d0e51b7f0c2c1b42848d8cf734d099643f7c6b9dc2ccafa6d42a666ccd50eeb933cf796391d6746d2dc629c563f0060d8c2ffb10aaa05b10470504a1552a1d33c1c6d86e82a0c90a4acc718201822b5d4942be5660384add8747b729ee8ff1e500dd0948e1802b5282bbc13aa75a5bcde896809257ec64f44f2b46c31f7fe544a1ee13ffd3b73fa2b61ad6ac67175444318af041ddb558313e5abd436bc679861f8f1b624e4a55054d9df2a4461b32e3429347aa46ce41fbe3ef80f4444e40d726ef06f66282857b4868af1addd0393230ffebe5f9fe51424afa4ce7677d2412a1c6da2f305fc60fb6599c7cae03f668ec9efdd8b0014251fe79c9df6050367f828ff49fe8d27e78570f798fabf7c938d63fdc82caef20f0c065a19270d0244bbe76afbcd940b49c5f446a1937e68845da77a39a41c83ab37cec5c410c377bb599d23189a063d8bbd24a32c405f8f0958319e9193fe1e4ccdc2e5feedccfab7ad9710139f0c660fa07cc3391364fd5fe8f4d8d376cbcf0c828a48389b43a38bf037d3de2e86f09f640543306c5df70cb1aa613a29fbd4868"
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