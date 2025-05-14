"""
Django settings for DjangoProject project.
"""

from pathlib import Path
import os
import dj_database_url

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
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd4qfmqaelhaou',
        'USER': 'ue3edpfcrvn1iu',
        'PASSWORD': 'p927ab6c7ca5f443100468557f9683b9b94ab0cfde3b745a42832502f43672c9e',
        'HOST': 'c5hilnj7pn10vb.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6ImViMTVkOWE0MzI3ZGZlMDRmMDgxN2ZmNzkxMjg3ZDNkZmNkMGM4YTkzZTdiZGZlYzljYTAxNDFjYTVlZDA2MzkyODZmNmQyZDdiNjRmMmIxIiwiaWF0IjoxNzQ3MjMwNzkzLjc2MDkzMiwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcyMzA3OTMuNzYwOTM2LCJleHAiOjE3NDcyMzQzOTMuNzAzOTg4LCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.mdNA8bPVqmNl3Pc4dvZBbJbig-urO6rlEl8WvPztkfB5K4ue_egjElZHU8MlM4496od1j4pWIPepAdC6CwVk1XjWYwl_kYQK11e-qi-YSudlZ_h7-YrOuacOGY-wp8y-5pTGGDkEdjW-aHou8JEy1EEuDnPgaq-oghgG2pk4iYPpZah9Ojr9E4LIE5SpYMxPlmbIEAYmw6E3oGSGFAWGukiKzIfS8fVubt82pC988OxXtKFs7qGOesSWZTg3mbm7au4e0_hOlGVD00l4xNwKFCfMcAzSQ--UBtAr07Ht47P7nhLUSdlwJfqQ9jXGCEpZQgcJoGmwUZuoO19hUjwLUA"
REVIZTO_REFRESH_TOKEN = "def50200c40087d40b479b9c4be060710f74816bd0c57e2f57c62107de278e1ac59fd43360756e1c63b195a762ff6765d0878eaf31cf31aec4bbba8e208b710f68ad9fb509180e633d9ca3d1d4e7a7f9e12045d60544fcbe4b2286b730ae85b785c15b021375fea9911eac97d222779b3a7b76208d3e3b2cc26d30000199ff6140781b9424a4d95ca88e7efe950c2c3fe002452f967d9545dd73180bf40e1a93ce240402838e6a27c738f49e99f3aae53afaac07fc798e4ec29045fe909c01964708a9b13cba6593e05955b5bf8c6c4f72eb217751f4704ebdab8313619099f37bc33faf27eebe5768636ec7ed274afc2773efb4c64c3d8dc91756b34c385d48bd44818f4809d282609fd5c7d6f416b3e21a4c80aff5d4db852f11d09d7f28cf69004e02eb28c21fda906cd72d006d15e77cd1b9ba350711be3f4922ff331538f36963db872b33e4dbb0d51cdb52b280108da9bd51caafe6782c5ba5bd92875a8050f01a756d761b06e869c4a48bfa3444bc44290cf76eb17484dc1c37f484554abee4547634a6c42d97f028e0cf23058ddeb08f4ec6882c50fba4f2dc0ea436ff36ea7a61cc9750753670d6e4268e8e1dd2cd47d82780069351a33a41c0fd3c90904b345a4ff4ce20332178702124f1cb602a54cb318278e70dc36514ad51db2d5c096f216f1fdde8efd673e00a674a52242bee071dfe4e9246c32cbc4c969c34ef57623d0c0803c6654d375fe9646f2a9f9407269c4a0e967fce076b586403deac38d625dfcf254158d794b1d7ac3bb0f4df20acc80f73fd3c28f375980c549affb6fe65bc5af1d6fbe99ac8e3001f915fbe605e0c670bc06d2e41"
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