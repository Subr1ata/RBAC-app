"""
Django settings for web_project project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
import random
import string
from pathlib import Path

from dotenv import load_dotenv

from .template import  THEME_LAYOUT_DIR, THEME_VARIABLES
LOGIN_URL = "/auth/login/"  # Redirect to this URL if the user is not authenticated

load_dotenv()  # take environment variables from .env.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", default="redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND_URL", default="redis://redis:6379/0")

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = "".join(random.choice(string.ascii_lowercase) for i in range(32))

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Default session engine
SESSION_COOKIE_AGE = 3600  # Time in seconds before the session expires (1 hour)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Keep session alive even when browser is closed

CSRF_TRUSTED_ORIGINS = [
    "https://marketing.galla.app",
    "https://www.marketing.galla.app",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", 'True').lower() in ['true', 'yes', '1']


AUTH_USER_MODEL = 'users.CustomUser'
SOCIAL_AUTH_USER_MODEL = 'users.CustomUser'

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# Current DJANGO_ENVIRONMENT
ENVIRONMENT = os.environ.get("DJANGO_ENVIRONMENT", default="local")

# SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('FB_APP_ID')  # Facebook App ID
# SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('FB_APP_SECRET')  # Facebook App Secret

# Redirect URI (must match the one set in your Facebook app settings)
SOCIAL_AUTH_FACEBOOK_REDIRECT_URI = f"{os.getenv('BASE_URL')}/oauth/complete/facebook/"

LOGIN_REDIRECT_URL = "/facebook/callback/"

# user_posts

# Permissions to request from the user
SOCIAL_AUTH_FACEBOOK_SCOPE = ["email", "instagram_basic", "instagram_content_publish",
            "instagram_manage_comments", "instagram_manage_insights",
            "pages_show_list", "public_profile", "read_insights", "pages_read_engagement",
            "pages_read_user_content", "pages_manage_posts", "pages_manage_metadata",
            "pages_manage_engagement", "pages_manage_ads", "ads_management",
            "business_management", "ads_read"]

AUTHENTICATION_BACKENDS = [
    'apps.social_config.backends.DynamicFacebookOAuth2',
    # 'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',  # Ensure this step is included
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# Application definition

INSTALLED_APPS = [
    'crispy_forms',
    'crispy_bootstrap5',  # Use Bootstrap 5 for styling
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.dashboards",
    "apps.pages",
    "apps.authentication",
    "apps.social_config",
    'social_django',
    "apps.users",
    "apps.marketing",
    "apps.clients",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'social_django.middleware.SocialAuthExceptionMiddleware',
    "config.middleware.LoginRequiredMiddleware",
    'config.middleware.MultiTenantMiddleware'
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.my_setting",
                "config.context_processors.environment",
                # "config.context_processors.facebook_credentials",
                "apps.social_config.context_processors.social_configs",
            ],
            "libraries": {
                "theme": "web_project.template_tags.theme",
            },
            "builtins": [
                "django.templatetags.static",
                "web_project.template_tags.theme",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
    # },
    "default": {
        "ENGINE": "django.db.backends.mysql",  # Use MySQL database backend
        "NAME": os.environ.get("DB_NAME"),  # Database name
        "USER": os.environ.get("DB_USER"),  # Database user
        "PASSWORD": os.environ.get("DB_PASSWORD"),  # Database password
        "HOST": os.environ.get("DB_HOST"),  # Database host
        "PORT": os.environ.get("DB_PORT"),  # Database port
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


STATICFILES_DIRS = [
    BASE_DIR / "src" / "assets",
]

# Default URL on which Django application runs for specific environment
BASE_URL = os.environ.get("BASE_URL", default="http://127.0.0.1:8000")


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Template Settings
# ------------------------------------------------------------------------------

THEME_LAYOUT_DIR = THEME_LAYOUT_DIR
THEME_VARIABLES = THEME_VARIABLES



# Your stuff...
# ------------------------------------------------------------------------------
