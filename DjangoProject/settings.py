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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6IjY4NjAxYWY2MzgwYzRkNDc2ODk0N2Q0MTJlMzFiODlmODU3ZWFmOWNjMDA3NjA3NDQxMDcwMDdjZWY2NmU3ODlkYjdlYTYwMWE4YWJhNmMyIiwiaWF0IjoxNzQ2ODE4MDE0LjMyOTYyNSwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDY4MTgwMTQuMzI5NjMsImV4cCI6MTc0NjgyMTYxNC4yOTA1MTgsInN1YiI6InNnYWdub25Ac3RnbS5uZXQiLCJzY29wZXMiOlsib3BlbkFwaSJdfQ.VIUAu7zc9yunExS0twdmqojf2dCQKDOQTefbjtT6z-HwOcwZn66Dgbsp0WlF6E4qFQDUqj8HuVIP0lxZALke21XVfISuRkrF98BfdyvJF7SuhdMyp75SHifm0iDF2ibbcP41t16qiQy8dWq1RFZPDgTc9VFnWuWhI9CqPZ5T7OZjZlwdoGsM9FFYHFUmH1M58rqBjfPS8p-0T9eUEOFfEk2cZeYoEh1KB70Jci0sWr5GPeDs7F2PRW7xK0gSH6CwapQziFBiqCaORvaeigO385wO8s0T9FhWaYjJi3ZPIDeBh7e_deEiqWIRQn2qnmToKqpGWIxKAf7xTIHRfbhPdA"
REVIZTO_REFRESH_TOKEN = "def502008fb087f2297dbed8fb30fef42904928b1ee385068f963d15050679c410ff8111a1ceeb486379257dae0332dc7bb77f19b0f566e635451dad2a6874146944408922f70ec1f1e172a59e621f67b6336a875de25f60d70ec665380cdee20b8f11ec4eb36f8cb6af5968b9fd7ab990e1f8f28ad6789279c64bbada4fc1874f499aa7c0f5ba5c47ca842c13ae8b563d0f914c2501027b3b727dec9de58609f7b3124b1fb8127a9ab6efebed33d93ed1d2e784dbb41b80d04dfb2c21ae2abaf484fc5c82e50b627bf946ebf678a30754231ece899d982e4c3050cde2e0b27d7fbca8760046e755705fc6d069710dfa0e1909a97ee63f05f04c5ed17aa84dd690bd41dbb582240a0652d9a8622d87b6812a2b88d84d85bfba98b6c3d52be1d728d51c431bb14496237649e149031f4e29f0fa20bc296b0fe430f91f7e0ac21e60157597b5ed189c9867493a0bebc2b2c568882c892a22d9c10f74bb728194e7169d1c1b38d5fae06c1fab4e11a1e68c51c89ef93e12474e1a69c219a70eae381a373d3cee4b9a7f19e8d4aff0458ba17887d38c039a67622cb431a325f2d81dcbafd417f466f62e0a0af0717ce6ae30c027af9953b7d09f9a80a2bc7f4273bf9cbde0a1ec36ab211638abfd74d3349eea049d9546df76f5319c6049d4687a186327c8383ecf194d529db10b92ec54c83ce887e19b7f66602c041c2363da2d8f6364bb579745c0c95327ab4aa03d2675b110e0cfa3655d244f83a4f6bf5ecd23de4d0fefe8c15da9358bc4778e458082b4bcde07c856f385751d9766b51a27f7b8f1ccc4ba21a78e00c5a8ae8ba6aa752a411f72c73eef251ee919ab"
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