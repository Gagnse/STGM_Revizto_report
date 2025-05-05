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
REVIZTO_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6ImE1NjM5NzQwNDJkYzQ0MDJiNzA2M2ZiMmVkNWY0N2IwZDdhN2MyMThmYTE3ZDZkYWVjNTA1M2M1MDE5ZDU4MDQ5ZjYyMzdjMzNlYzU2NjBkIiwiaWF0IjoxNzQ2NDcyODI5LjAxMjg1LCJpc3MiOiJ7XCJob3N0XCI6XCJhcGkuY2FuYWRhLnJldml6dG8uY29tXCIsXCJwb3J0XCI6NDQzLFwicHJvdG9jb2xcIjpcImh0dHBzXCIsXCJ0aW1lem9uZV9uYW1lXCI6XCJDU1RcIixcInRpbWV6b25lX3NoaWZ0XCI6XCJBbWVyaWNhXFwvQ2hpY2Fnb1wifSIsIm5iZiI6MTc0NjQ3MjgyOS4wMTI4NTUsImV4cCI6MTc0NjQ3NjQyOC45NzA1MzcsInN1YiI6InNnYWdub25Ac3RnbS5uZXQiLCJzY29wZXMiOlsib3BlbkFwaSJdfQ.CVkT1d-xXoMxVRHPFEZdLHex2ZY3vXlJtu5Im3Ex06g1QjRxm48juloqXg6PXlLv8kdJuU9uoeRoWg1akv-8XqeV1Hxe7OK-rCQKEaxRfhWW2MSwv1sxDn3G2U0tlZJAqQEXPInExXhrCJqnj2bke9HwvKvEaZdM7yjjsZNwSslY5wBCJ425pwcM6PUCYBGcvXNl0ndB-Du5Sxi6NGslg3Eofh_2T_H-UBOvYsI_RW8mjOrWE8bkgNcWnW5R3DHkRMir4zWd4P-AJ7UU0BoWMSH2-4Qui6-Gs0TT3EYCn84EWdisMSPOmnCzxaEKTrz76raXEC2RgaBcbMYoFzj2Hw"
REVIZTO_REFRESH_TOKEN = "def502007b6bb7ef57a7ca9913261c1f922c27f20af9e4470e156191882b74c6ef5fd535fc0258bc719f73870981434976c511f7781ff107f9e1c202e14f98cd854f3ff18c94941804e6a0b5ac2e8ad3764e72d1dd6dcc6f508038529224dd8c860b8ad728c14304708c8d25d1a82ef1546cb872aa6964634526dcdc4d4fd115274ebb7a63733fdbeafbe5790890f18e3851af0cd5a803a67b4450af83dcab1553e89097907efac926324041e135128b398c49c1024232de3e6ec5c2cfaae8c5bcc2acfad59bd3f0cb6caf935b5a2c973dc8e3dd72e945bf4df20a7a88d4c2680b74e2f697d3469cffaf1bbee0fa2366fdd8c8af5b598221865f75ce3ed7c431170611c75d4dc91705024f769d9f1a8290e01c9c8f161cd6054c72538c3dcf1ea86983966e687e76b42b41a16a192e5afbc4ec49ded0f9da956feaa4e808eca64214c5fd1809ac1e6efeddc4e5b9f6c625eff6053f5d66ecfb77dac09f80b86f9c4c098d644af5cfa95ecfaf3c22118aa976bd46e58dedf19208d0507b90bd3263a32b42194a737a2c47d3fedd946c55ec69d5059f72c60c860774af7621a3249b9d4a449b33d336e87c134f1b65f9c10dec39b7a41e4acab7d9cdc89c42a8c22e7b66ca5e9483d6414021d555d5843f2fc603e61334eccc39a7cd1e5d0c00b02b54c61888cf78fc13c95b5a56b7b3a91efadf0ee2556926bf2213f8d2e207c4ec821dc9cd6e672c7ce99f948c6586ead3fae4ce2a64b4b0a280c47ccae811796fb8aaa0d4d4d624eb5d4784ae16ce85d8d2d5438de5fef5816b034d35d889599dca6fdbd2af853c9d4f6ca3d89ce3b0bcd979e2189f0f2706e42e5f"
REVIZTO_LICENCE_UUID = "2e38d742-c9ad-4d11-b5a8-c9b53e9bf517"
# For production, use environment variables instead
# import os
# REVIZTO_ACCESS_TOKEN = os.environ.get("REVIZTO_ACCESS_TOKEN")
# REVIZTO_REFRESH_TOKEN = os.environ.get("REVIZTO_REFRESH_TOKEN")