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

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'stgm-revizto-report-50fd6709d791.herokuapp.com']

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
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

db_from_env = dj_database_url.config(conn_max_age=600)

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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # This points to your static files directory
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Revizto API Settings
REVIZTO_API_BASE_URL = os.environ.get("REVIZTO_API_BASE_URL","https://api.canada.revizto.com/v5/")

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.herokuapp.com']

# These should be set in your environment variables for security
# You will need to provide these values
# REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6ImM1MTE3ODBjYTM0ZWQyMWM4OTVlOTA1ZTM4MzU4OTc0NDljMzMwZjgwNDdjZTlkYTg5MGQ4M2Q1ZTEwY2EwMGMzODk2NTAxZWQ5ZWY0ZGIxIiwiaWF0IjoxNzQ3MjM1MTM1LjIzNDQ2NiwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcyMzUxMzUuMjM0NDcyLCJleHAiOjE3NDcyMzg3MzUuMTgxNjc0LCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.btLeBBnhTnmKSesYbFY9FdwlT_rSIZ2D4rTY8hp6Ut1Ha6itq8UPbI9WtOr-K8T7HsWU-lsu7HQxOih6CUhJi-aMJjML4Rkh3geyFzs5vAyQuanwKalKTjubqOQDUMKcXekvCcY_SHPOxuFAC38V6-5K4cY0D4eU0G1uj5vQUJ7Itk3uUb0LpLa0QpXZ9m3j0deKqmDDRNdMPkWuruNKtbC2bXepy08zXeA_cSe9l4rqbmly19EQ4gt0rLNiUst0Paq8hUqTA5op8yglGmmtWJn2WLwEJFcdOk1xu7b5q2iczIpKrZCVnJ7lQNqbAh82D0L6KYPc42v-ZK467szCMA"
# REVIZTO_REFRESH_TOKEN = "def50200dce2a0c31a3a61a71b5b0b006f27265138a405449259bde277fd051f980f26d6406e1013163da48eda530def728f5bd09105b185bc743f8b483e94a7e4fbb0949e61f447885bf5d2856c2df84ac958512dd8ed1fc61b664733c6fe4a146bf1ff42c6db2a8c8ac84a6eb34ff9821bd4102be5dcc5c1f06d966d8d15194d0e07744db35124bda0e8fe1f7df0394da4a48e60adb90b65bbd865d30ebed7ab3bff648e9f6ade38d8b24d52e6144e0393d10f77bc15a5feaa95fbb83566fa5158f003721881f3ad6e054071774a87d42a78dbba8302fb0dd9341c5e252c3126fa7e0ebef999ee697104619d9340e99b4233988fb7e62e7fd48d40f5e486dfe2c42e4ec7a3bc29ce91d9c7abf7bb20873174644037e522d9cdcd9c22ae55ed56203c73f8e83a3472af0653dd01ea6334def5a4e6513f1c09d440dce64adf71604c2b7057112c9a20d65c023b83366e62f05e8be36bd4ac817dfe666616d39844851f57c3f9d79fd3f6e5100a340f59ff1b631c5483d4ad2f49fb482ecead97050c3782c3790fb171afda086ab175b8a234e5d572cacaf2b2cc64d89d2bb33323fa7fd3b252db232e9ef84d304fefb29448b1931f951828c94c1401d97db088f0401b271e7b5b2118ab48fa1b030b8b91052f1dc2ab068e0666abab045a36f99f61628070636f3b168ccb94489d0fbdec704fab0310f27d6b7beb1c2b78945cba578b91e3390cebc975140f6c0a6ae38af0fed40f2baa6fb56cfc9e19ee78f8e1a3b836cf36989c224881978fa9c9ee6c4060296d228024f4cfeb5807866fcbb2d1dafcaacf2ab218a110db1545555a48ff7affef18a06f2b24430f"
# REVIZTO_LICENCE_UUID = "2e38d742-c9ad-4d11-b5a8-c9b53e9bf517"
# For production, use environment variables instead
# import os

REVIZTO_ACCESS_TOKEN = os.environ.get("REVIZTO_ACCESS_TOKEN", "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6ImQyODNiMGYzZDE0MmNiM2Y3YjBmMmE0ODZiMGE3OGRiZjZjNDQ3OWVhZTdiMjBjZTcxNWRkMTZjMmU4NmJjOGM2Y2E1ZTYwMGQ3ZWExOTc1IiwiaWF0IjoxNzQ3MjQyMjE0LjYyMzYyNiwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcyNDIyMTQuNjIzNjMxLCJleHAiOjE3NDcyNDU4MTQuNTcxNzY5LCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.DaDMHQ06q7YTPgSdsJpIimPWsw9d4JWZUHfYx6YLlOfaynyhNZ6tXqA_x8D_JlWo4D8S5QveaUunOzHJsthRKfrYlE1b6vD_nAN9nNSeLtDAbCzXwxItXaNG2uOMmsD-HaUW5yKJm4fOviWr1LR0FmRWCLMtrVhxyk2CQGj1tKVr5FuE1JxfpTOuVeSOjFVC1b1SQKWrk6QU6gG14-w4YB37iX-xHJRzpoVftFYtZODiM15YJR9wPy1yprf1qm9TQtrNJAqW8xIDBdYrBXZTHbvoTlqPJ1u7ica6JABCnQT__fN5x1bLbe9sqct0sNHT3f7UoWkmZoveZ9zYzFLzEw")
REVIZTO_REFRESH_TOKEN = os.environ.get("REVIZTO_REFRESH_TOKEN", "def50200a5ba8867332c6c09f6a90010d110df68a8e0966d8c7d8386390e34903f1565a985f0229bde9f036428c385670539b429527d0c7a31fb21f7bf397cce88c61acddb7cb31a61eaefb190f21539f9e06f3735833c526084572829fc56252f6df0521654ce7aefd6131c58ad1a422b861a1c91a4e3284b87918bd1c64a6cf908316adad5f86cbc1df867ceec6b5efb48a865f83f8f4e314189299f2554f670ed02bcedc30e0b2bf8ee9a1d3e6d5caa0b4c986d37c87ab8e5256c45fc889847c8466b5b2d51563350207da4a6fb901a4f849e7926466dd7ddab14a03a56aae8db8bd9ea8dcd0ce9d775756569d226b6b3d1a34bf33ee56b61bf5d70032240e58c9002ac38fe60e31acaec643530ad57f225eac489a64a4ef4eccfb8de17515858de84caf89c5f723d167486113d35e9ff6cacb2e74fee87102e0ca6ed0dfd6a8eb36d74f2ef78ed642a0ec0a0e0719ab11cbb59ac609a78d1919ee2a93ab25e1278c55085a4904f531ca31302a62f0c1303c904037f47e8959573c6e50eee2e9fd85d809c0d1d301848e3a34be90760e41be8e02b065f02c1d7442ca22d2861e17d63739ddfcbfdf3ad5c503753f4f7fd17599b423226095d19d2d38d591128ea9b3f9a4c4de13809abbf52147e36f46661254442437085b52208cd8b4b28329671d8f5cae0961f0be4667442b4fd84f59dd166e2cf8c84236d00fe3ed235e3d00d5778742673be31db315d52288e11ca68d0bde61368d189f3a5a57c6ffa91ef6e7b30e8596504525c0f7900761dbd37cc63bdcc3d5c923159fbb32db43ec7b4f7c9556cee5b824f9b4d09896f3de8db25a671b7217c0f524227")
REVIZTO_LICENCE_UUID = os.environ.get("REVIZTO_LICENCE_UUID", "2e38d742-c9ad-4d11-b5a8-c9b53e9bf517")

REVIZTO_ENABLE_TOKEN_REFRESH = True # Set to False to disable during developmen

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