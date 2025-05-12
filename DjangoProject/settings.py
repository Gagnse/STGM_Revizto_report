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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6IjRkMGJhOTk2YmY4M2ZhODIzN2VmNGIzNDlkYmMxNDBjZGE3NWI0MWE4NjUxM2U4NWI0MGZjZGI5YjNkZTEzYjI2YjRjMjUzY2M4NDY5YjhiIiwiaWF0IjoxNzQ3MDY1NDcxLjE0MTU5NywiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcwNjU0NzEuMTQxNjAyLCJleHAiOjE3NDcwNjkwNzEuMDkxMTAzLCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.M51K8KV06HUBPDRnRMfvHSDBo58gDob0Sl-hAQdlL0r_DqiYnLzsQTMrcis1gOxRbjqPkX1JqKfHGr_vLHYFxFDWatRpYnJs8RqL50NcYleAtwpgQ8wOtgi5qjWvizXwziP3iQBXOiEZ2coNv5icWnonKcalOWZxszVGU-IqSJH21zgPx05C-u2MH9vRC_lP5Olj0Ouz-P4x4bEu87VuPooY1OGShaK2Tan5gXGVC3qXtjPw1LQXIQAi3r28oEFVJfs5Q4CksnTWQodBEMc_BB9b_t4blDPhxtctoBLErs-x3UR7s_k8i7TDnizjZEzevhUQZxZLY0EX8lzmsRgdYw"
REVIZTO_REFRESH_TOKEN = "def50200d43130058fa77b069178b5fb45ea635ce7481b870d70794e2bbe1e86b5a23ab877af7d20b5abf7172015abadd167ce506837f2b74c235d8ed6a3a570b6a6d5f0b85954e89654234dc5edb581ce42e6231710c1cb6d14665bb0a62bde596339518efc81911932dcef637dc12ca469550b7502e3d0efe4209c3ae7c0e8f6487e8011743696328faa5e76f00c6caf86ba92146432a586dd8a2f206a3d4e9e1e0c1c6efc4b9dafe09985265b230a2bf7664e5b971c4212e4302a47d1298c72c5a628e07a6ad396d58e55a098e3aa429465f6e74ca585ae1abf48a824fe1ed41d8a830abc367d0fbe56d066b6a6dc690e48f661d3ecdb6fe88d0ab098713f471232e6ac2b9b7de71eda64cf6fc8f2abc6f8d473a01a5a1d4eebfcac2205eb35758451fac3d5566f6a3e145067eac65874615d993305705e662425e51284ad2ad88e300a6765e4f11ba208cf6d40cb4ce39a6140f57d5770a37aa964a69a105e66ab2c0d27fcd4484eff669e8798419cf1e0d9b30b3bf9c19adfb4f982d226e8c9cbc078c71e3d63d592506853416fb2add216b8e68f373943b31d7da25b96ce3ae609db5a414f6f60d045522a81fb7d01e9a3f40672065a86826d96dc252d25449db81c95eebef9bc2f7ff3fef947ad11943d903ba7ad9ca1011688a34974eb56f57fad7410ee4999d9199776a553ae8dab6f55a1e5186d5c72b82b6fe6fb542afcc8e3a81e8c9b7d098446a7e0a015aaa917cd87e01aadba3c26e57a96f61f33a6dc3131b44df5e85e812f1af0d1f0d4787247f99d2c18c77992435818d63ca75d7537abec67e23b50691e51e63eb1aaf035e7dc342c5601985f"
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