"""
Django settings for inn_project project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fantasy-inn-tycoon-dev-key-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'game_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inn_project.urls'

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

WSGI_APPLICATION = 'inn_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        "HOST": "51.15.160.236",
        "PORT": "49432",
        "USER": "admin",
        "PASSWORD": "85af6f3f99864132343a5f0434a12944edc",
        "OPTIONS": {
            # "pool": True,  # Commented out - requires psycopg-pool
            "server_side_binding": True,
        }
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings for Angular frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "https://ofm-inn.netlify.app",
]

CORS_ALLOW_CREDENTIALS = True

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

# ============================================================================
# STRIPE CONFIGURATION
# ============================================================================
# Get from environment variables or use test keys for development
STRIPE_SECRET_KEY = os.environ.get(
    'STRIPE_SECRET_KEY',
    'sk_test_51234567890abcdefghijklmnopqrstuvwxyz'  # Replace with your test key
)
STRIPE_PUBLISHABLE_KEY = os.environ.get(
    'STRIPE_PUBLISHABLE_KEY',
    'pk_test_51234567890abcdefghijklmnopqrstuvwxyz'  # Replace with your test key
)
STRIPE_WEBHOOK_SECRET = os.environ.get(
    'STRIPE_WEBHOOK_SECRET',
    ''  # Optional for development, required for production
)



# ============================================================================
# OPENROUTER CONFIGURATION
# ============================================================================
# OpenRouter is a unified API for accessing multiple LLMs
# Get API key from: https://openrouter.ai/keys
OPENROUTER_API_KEY = os.environ.get(
    'OPENROUTER_API_KEY',
    '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'  # Add your OpenRouter API key here or via environment variable
)

# Default model to use for guest generation
# Free options: 'meta-llama/llama-3.1-8b-instruct:free', 'google/gemini-2.0-flash-exp:free'
# Paid options: 'anthropic/claude-3.5-sonnet', 'openai/gpt-4o-mini', etc.
OPENROUTER_DEFAULT_MODEL = os.environ.get(
    'OPENROUTER_DEFAULT_MODEL',
    'meta-llama/llama-3.2-3b-instruct:free'  # Free tier model
)

# Enable/disable LLM guest generation (falls back to traditional generation if disabled or fails)
USE_LLM_GUEST_GENERATION = False#os.environ.get('USE_LLM_GUEST_GENERATION', 'true').lower() == 'true'

# MQTT Configuration for real-time updates
MQTT_BROKER_HOST = os.environ.get('MQTT_BROKER_HOST', 'broker.hivemq.com')
MQTT_BROKER_PORT = int(os.environ.get('MQTT_BROKER_PORT', '1883'))
MQTT_USERNAME = os.environ.get('MQTT_USERNAME' )
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')
MQTT_USE_TLS = os.environ.get('MQTT_USE_TLS', 'false').lower() == 'true'
