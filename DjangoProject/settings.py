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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6ImNjOGEyMjI1NmE1YThmMzY2NDk0NThiM2RlOWRkMWQwZDM3N2U3MmU5ZDU3NGE1MTRmOTlmNTAzMGM5MTRjMzk1MDZiOTNiZjhlYWUwMmU3IiwiaWF0IjoxNzQ3MDU1NjczLjA0MTE5OSwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcwNTU2NzMuMDQxMjA0LCJleHAiOjE3NDcwNTkyNzIuOTg5NzY5LCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.N-t8LQLfNFqSn3dn2UMBDKA--UE8dL-OFqqnJ0YAUJRwF32Sh_RT4JXGzI1weMJU2enLOW-n_bcrMsm9Dz3rq_ZUEsjxJ2rqRwR6gOEnv1WHGP3cDiPmB-mJE04FTb2uPOSWHLqop9lDlbWjhizgbRmqpej9qqq5ym7eh_B6IAsQrrHlXS3onlY_cMWBHMrQu5AKkRxQYyyY37FQtUshQwpbp1ysxEhi7H7VZ-M5avgwARisaVD7UIA9DcHSIHIIcoI61Vp_wQEtu2q4ak6v7yCH57VACe7tltov2WpJ4tnZ_RCdafxXaFWYQAjb68txWzk1p66BR2HDt70nyROt9A"
REVIZTO_REFRESH_TOKEN = "def50200ff75b355934b2d3dc16b20af85d9c63ad38b882b21ae53b6154446ab5114f69dcc900f248526f81ebbc4d3f9434b6f93f134b75869e5f696272781e6a75b5848601af1d7893404d70caccf09f86e6839fdbea79df1dab5e5d363089b39f82d2d8a6273d65166e8ac802f37f5b739910a8415611c79300823e34efb08c4935991c3616cdbd863e568f8108270130a4cbd6e96cd77f3b6d15ada2c0ae5367bac43da024891b2cd76ebb5ba74156c35d95ed71a8a4cbe69e64e48dbd36f1dad99e74eb6d97b07f4207c2c5c927cb8e8e2d1bc6ff8062c41edae06a14b74eb5a929b01a9e0677686d577e1fe085908242751242feb9db41486dae82e51fd48b73f5994e6233e5009eaa6c0ae03ebd2ba663a78898f17aeed34e116b2735948b7981745f9b8d1b03b0b7cbb44eb48d459e8eaab5bd607b41ddb7e696a20367231ffb54ea7357cf088fb6c5e2b533e25775c4c4eecd29c2e5bf7edacf29229d25975215f74ea69798192d89d8dffdeffe0bbfcd25504fcf0249d6a0a742d16595d0896d56bd529293b6112ad23f95066277b848e5fc40fb5b7244247cf6083e5723aead9c44998503b44422d9398580baf7cf929026a94143953e15145121b321b84e2fd7062ad8f3bcfc0f926163177eeb72f3258cba2b29ae1fa4a32da29345b55c743da4be26d0696c206bc8adc198acb15d6ceb5603a21c6c46de5149bbb49f54336f62234184d02b9fcfb60379f8651e5f678973e774da53391ebdbd6db79b0826c5a0b8e33d4af6daa7730543e94f89df425ae0b6726e736157304347c5daf9b4f0ebdd4e1fdc114ceb7e04aaa29aa32846c92ec1e9b46b7"
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