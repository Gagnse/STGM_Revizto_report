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
    }
}

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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6ImE2Y2M3Nzk5ZWQ1YWM0NjQ0NzNiYjY2MWM2YmM0NWJkYWM5MzRiMGViMzBhMTkxMmE4MmNmNjQ5NTk1ZDNiMjI4ZTJjMmU1ZWY2MGM3YWQzIiwiaWF0IjoxNzQ2NDcwNjI4Ljc0NjA0MSwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDY0NzA2MjguNzQ2MDQ2LCJleHAiOjE3NDY0NzQyMjguNzA2NjEsInN1YiI6InNnYWdub25Ac3RnbS5uZXQiLCJzY29wZXMiOlsib3BlbkFwaSJdfQ.pXj_XlacFN7QHwCr_whhyJJfV3zrSET7pH2FxuOyaNMXFVAZhxssNwIXBnw-iU-gfoHWS3m1VZcoyPNnHlLxO1GvCTJhwmK2OsbGD60JApg1Az9cj5ZFpHOJx_x_LLTyI_MgL-Mm0DYIOzi0t3mEkm-MBlTK3dXalyyMpDrQBdoFrhYdhEFwtW7dsqL0VhmOQqISpXAHqA5aiwQUS0TaWVxNw3nZ-W43yF7YJ1L8qOrjNLfBx_OfQQ2s2I5SJTBmVQ3hXcy_KCUPb4pcavTq7GthLMVWnSRKN19IdOCPcL90AjuxyqfEzimtNVOJvhkezcNS_A_m1fpby8BBL5yZbQ"
REVIZTO_REFRESH_TOKEN = "def50200ec7fafcb684c8f494c8098b759c227f8c76d6e13c447a2ff2dc892f7a13125b83da169fd5227a5192741c9a0c2c98668be4c061912395bb974aa1d48b5b7f59b6dab6855374137a519fcd42515d9e8dfc8a4e277cc996992c098c11bc6fc1a71eb78b40960c0b4f585fa13a57a34df8afe8aac1a084ab62711b6fe6718d9fe08966bc8cf3988cedd5f59dbb8eca852e3dbfe8fe5d1ceb2ad2add5695d681de8d300b5a364349722a96f3685617add69ac5fcda6049bdef47279adfabc55b96f91de06e19379100f5ee73f02e439a4d240a44de5d1a965928798880161434b88b0cd19d61a13bc66cc227be9ca3d6248c92a5ec1a9ffaaa81abb75971c06dbe54c0632188397e8820f1e79e7fed14befe4e1e2fe0e4ef762691bbf8f477f6dcffb2713f66bcdd181b21a1ef275db3658b2a1e6e8a02a1d9367912a491da6547b701d7698562253c3adbe324959c89ccc453480e704be56e09fd465cbdce552d572f72a3db45bfbee5f7aef09b68c23d242a9a7f737012c82f3cd26f3753260a9b57da8bb5f78e32562d3cdef25c428678cfe3ac4af8f5a371455fbcefc3df723526f0eab797009b3ff92ef0abea2018b37ed1ba8225a9d35d29c1f2856958700fad4158c939acd736d363329466d0b9c3abe586b714e001ee55b8c0a715cbe1088f0c1b9afcbb0a5b0ee7e7a522cfbed8655c3d4e7c93076b44137d0a14cd1fb5994c259fd1400c0c0fc6ae9ace0020543a358e45e6b553fa7e4a4d02ab26625a51a6c7deeb6e79c0af2cfe082939924729160465eb89a577c6a14cf949a9f1fc3d91a4cef16fcf197502f33fcb492a783ab365f4bf5800a9"
REVIZTO_LICENCE_UUID = "2e38d742-c9ad-4d11-b5a8-c9b53e9bf517"
# For production, use environment variables instead
# import os
# REVIZTO_ACCESS_TOKEN = os.environ.get("REVIZTO_ACCESS_TOKEN")
# REVIZTO_REFRESH_TOKEN = os.environ.get("REVIZTO_REFRESH_TOKEN")