import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+s8j@uh%)p9^7!^w456browv28mjj!bz&e&bzq!9@lxs^+zdsn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Update this line in your settings.py
# Update ALLOWED_HOSTS to explicitly include your domain
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,api.roteiroibiapaba.com.br').split(',')

# Fix CORS configuration - remove the conflicting setting
CORS_ALLOWED_ORIGINS = [
    "https://roteiroibiapaba.com.br",
    "https://www.roteiroibiapaba.com.br",
    "https://api.roteiroibiapaba.com.br",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
]
CORS_ALLOW_CREDENTIALS = True

# Remove this line as it conflicts with CORS_ALLOWED_ORIGINS
# CORS_ALLOW_ALL_ORIGINS = True  

# Update static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Use a simpler static files storage for now to debug the issue
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Add this to help with serving static files
WHITENOISE_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Add to INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',  # Add this line
    'django_filters',  # Add this line for filtering
    'corsheaders',  # Add CORS headers support
    
    # Local apps
    'users',
    'tourist_spots',
    'favorites',
]

# Add Swagger settings
# Update your SWAGGER_SETTINGS to include static URLs
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    'VALIDATOR_URL': None,  # Disable validator
    'DISPLAY_OPERATION_ID': False,
    'SUPPORTED_SUBMIT_METHODS': [  # Methods supported for try it out
        'get',
        'post',
        'put',
        'delete',
        'patch',
    ],
}

# Make sure WhiteNoise is properly configured
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # This must be right after SecurityMiddleware
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # In production, you might want to restrict this

ROOT_URLCONF = 'roteiro_ibiapaba.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'roteiro_ibiapaba.wsgi.application'

# Database
# Use environment variables for database configuration in Docker
if os.environ.get('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'roteiro_ibiapaba_db',
            'USER': 'postgres',
            'PASSWORD': 'soeusei123',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# Password validation
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
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Fortaleza'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Fix the typo in STATICFILES_STORAGE - it says "statvicfiles" instead of "staticfiles"
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Make sure to include all app static directories
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Remove the duplicate WhiteNoise storage setting
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Keep this setting
WHITENOISE_USE_FINDERS = True

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'users.User'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'