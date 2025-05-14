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

REVIZTO_ACCESS_TOKEN = os.environ.get("REVIZTO_ACCESS_TOKEN", "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6ImY4MjM5MzEyZmY1Y2E2MjQ0MmFhNzhlNDk4ZTM3Y2UwOGFiMGYyZGZjOTc5NzZmYWQ1NmFhYzRjZGY2ZGRkYjNiZjY0N2E4NzRjN2E2ZjRkIiwiaWF0IjoxNzQ3MjM5MjI0LjA3Nzc2NywiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcyMzkyMjQuMDc3NzcyLCJleHAiOjE3NDcyNDI4MjQuMDE3MzgsInN1YiI6InNnYWdub25Ac3RnbS5uZXQiLCJzY29wZXMiOlsib3BlbkFwaSJdfQ.ej15AqXRUfLG1BOQU9mBOyoALkOl_M1toysFIomNWbordQ6yOgwUm2kDxPEO_maFJUcsbrLzuoRW5m_HIrlDd8bdIF0x6kLkk_mG04U1OvVilu1J3NFVuSFTdRRqT-GCFRQgjdBYdy5SqwRwCW951sWPCKA_HR1UXHBcGne05thvLFB6RfJmUSyv-f62BKlZV87F21N7YIn1HgdVujz8J7aqOfUqcbVbQ2_XBAHw-PTCEdGE-Ojl2GirqHwWfF0QlC5XJiVB-9rq6EHDVt2kq8PMv0E0VsSHs3KERbtPgEU-VpjU-7_ywMCkOQXhGSXi_jahItzd9tepwdFTjscHiQ")
REVIZTO_REFRESH_TOKEN = os.environ.get("REVIZTO_REFRESH_TOKEN", "def50200e54f1e305d4283a0e613c16750f89df6fb7646c9e683cf55cf0e47bca590c6690f447e8531f104d8014db2323fc98a0298a6adf393bef61ddabcae894a819219eefcd9aa33d861b9ddbabfc808b9b06102b00354005c5abbc1390c4dcc827f35a3b1db662241b56df26b82277c69716b35ac836f8bfb58d1c4d43afec9f401a4e60dfc9ce9732039288c0fe79d78b254f4a8ed1b1b0e4b4702cd52d50cfc15f278a626e23746b5f437f9bbebf2d140001bbcafb78c7d4f12254318610c1ce983717585a7fd3ec73db40207ebbf49e7053412e556a31c7d0b08f7ff039402f84b768dcbb153ac29d6a0a6fb1a275a5aa45412bfd36b7c17cc4accaaf819995e45e6cc07392ee3203842aa14d5201ed9dc286b95ebc8caac0b0fc5f8cf217a418f7a065d8605921280faa115efa98e5748b6c567098b39700ef43b3be11ef059f3237dd631807f0b11038472e9445d11cccd3846fb32ed02d6bbf2232f769e0c19f77f613f71094367db3151611881683d58268924533a2ee732eed53619daf4eb6950c6c1942f082b9af3d25d1b3f4a76ef558f84d1600113e4865d61b0ff08550e8e40c24a30fd8fb2e3ea8dba72689a340d536054a46e4bcc43598888d2232e46ab0a87541876b2e14d56f4cb9410735079e69f3898a79d97145ffaf5f83ae3595e40591a3d1eb6697f5cec718806b4b20e875117578b37b1c3f101f2c68c986497d72dd26cc2d0da9668f1412472742e0adb7f52d01189fe1867c9ff42fe88be762cd7ba478fb462a249629fb0226cec1feb0f484f79cfdc631a635130aa426fe80d27cf12136ec84a6748ec54c4bb8166b91cca320aea")
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