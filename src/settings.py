"""
Django settings for repository project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from src.env import *
from src.auth import *

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = '' # MEDIA_ROOT + '/media/'
STATICFILES_DIRS = (root('data'), root('media'))


ALLOWED_HOSTS = env('ALLOWED_HOSTS')
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

APPEND_SLASH = True
ROOT_URLCONF = 'src.urls'
WSGI_APPLICATION = 'src.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {'default': env.db_url(), }
LOGIN_URL = '/signin/'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
LANGUAGES = ( ('en', 'English'), )
SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*10,
            'backupCount' : 10,
            'filename': '%s/cache/log_django.log' % MEDIA_ROOT,
        },
        'email': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django_crontab.crontab': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'src': {
            'handlers': ['file'],
            'level': 'WARNING',
        },
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
        },
        'django.request': {
            'handlers': ['email'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['email'],
            'level': 'ERROR',
            'propagate': True,
        }
    },
}


# Application definition
INSTALLED_APPS = (
    # 'sslserver',
    'django_crontab',

    'filemanager',
    'adminplus',
    'suit',
    # 'bootstrap_admin',
    # 'django_admin_bootstrapped',
    'django.contrib.admin.apps.SimpleAdminConfig',
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'src',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'src.auth.ExceptionUserInfoMiddleware',
    'src.auth.AutomaticAdminLoginMiddleware',
]
if not DEBUG: MIDDLEWARE_CLASSES.append('django.middleware.security.SecurityMiddleware')


TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'DIRS': [
        root('media'),
        root(),
    ],
    'OPTIONS': {
        'debug': DEBUG,
        # List of callables that know how to import templates from various sources.
        'loaders': [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
        'context_processors': [
            "django.contrib.auth.context_processors.auth",
            "django.core.context_processors.debug",
            "django.core.context_processors.i18n",
            "django.core.context_processors.request",
            "django.core.context_processors.media",
            "django.core.context_processors.static",
            "django.contrib.messages.context_processors.messages",

            "src.models.email_form",
            "src.models.debug_flag",
            "src.models.ga_tracker",
        ]
    }
}]


SUIT_CONFIG = {
    # header
    'ADMIN_NAME': '%s Website' % env('SERVER_NAME'),
    'HEADER_DATE_FORMAT': 'F d, Y (l)',
    'HEADER_TIME_FORMAT': 'h:i a (e)',

    # forms
    'SHOW_REQUIRED_ASTERISK': True,  # Default True
    'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    # 'SEARCH_URL': '/admin/auth/user/',
    'MENU_OPEN_FIRST_CHILD': True, # Default True
    'MENU': (),

    # misc
    'LIST_PER_PAGE': 25
}

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
if not DEBUG: 
    SECURE_HSTS_SECONDS = 31536000 # one year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_HOST = env('SSL_HOST')
SECURE_SSL_REDIRECT = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = (not DEBUG)
CSRF_COOKIE_HTTPONLY = True
# X_FRAME_OPTIONS = 'DENY'
