'''
Django set for great-cms project.

Generated by 'django-admin startproject' using Django 2.2.6.

https://docs.djangoproject.com/en/2.2/ref/settings/
'''

import environ
import sentry_sdk
from django.urls import reverse_lazy
from sentry_sdk.integrations.django import DjangoIntegration

ROOT_DIR = (environ.Path(__file__) - 2)

env = environ.Env()

for env_file in env.list('ENV_FILES', default=[]):
    env.read_env(f'config/env/{env_file}')

DEBUG = env.bool('DEBUG', False)
SECRET_KEY = env.str('SECRET_KEY')

# As the app is running behind a host-based router supplied by GDS PaaS, we can open ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']

# https://docs.djangoproject.com/en/dev/ref/settings/#append-slash
APPEND_SLASH = True

# Application definition

INSTALLED_APPS = [
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'taggit',
    'storages',
    'django_extensions',
    'directory_sso_api_client',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'sso',
    'core',
    'domestic',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'directory_sso_api_client.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'directory_components.context_processors.sso_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {'default': env.db()}
DATABASES['default']['ATOMIC_REQUESTS'] = True

VCAP_SERVICES = env.json('VCAP_SERVICES', {})

if 'redis' in VCAP_SERVICES:
    REDIS_URL = VCAP_SERVICES['redis'][0]['credentials']['uri']
else:
    REDIS_URL = env.str('REDIS_URL')


if env.bool('API_CACHE_DISABLED', False):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }

CACHE_EXPIRE_SECONDS = env.int('CACHE_EXPIRE_SECONDS', 60 * 30)  # 30 minutes

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    str(ROOT_DIR('core/static')),
    str(ROOT_DIR('javascript/dist')),
]

STATICFILES_STORAGE = env.str(
    'STATICFILES_STORAGE',
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)
DEFAULT_FILE_STORAGE = env.str(
    'DEFAULT_FILE_STORAGE',
    'storages.backends.s3boto3.S3Boto3Storage'
)

STATIC_ROOT = str(ROOT_DIR('static'))
STATIC_URL = '/static/'

MEDIA_ROOT = str(ROOT_DIR('media'))
MEDIA_URL = '/media/'


# Wagtail set

WAGTAIL_SITE_NAME = 'Great CMS MVP'

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = env.str('BASE_URL')


# Logging for development
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': True,
            },
            'mohawk': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            'requests': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            'boto3': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            'botocore': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            's3transfer': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            'storages': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            'wagtail_factories': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            'factory': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
        }
    }
else:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry_sdk': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False
            },
            'django.security.DisallowedHost': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }


# Sentry
if env.str('SENTRY_DSN', ''):
    sentry_sdk.init(
        dsn=env.str('SENTRY_DSN'),
        environment=env.str('SENTRY_ENVIRONMENT'),
        integrations=[DjangoIntegration()]
    )

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', 16070400)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', True)
SESSION_COOKIE_HTTPONLY = True
# must be None to allow copy upstream to work
SESSION_COOKIE_SAMESITE = None
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', True)

# security
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# django-storages
AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME', '')
AWS_DEFAULT_ACL = 'public-read'
AWS_AUTO_CREATE_BUCKET = False
AWS_QUERYSTRING_AUTH = False
AWS_S3_ENCRYPTION = False
AWS_S3_FILE_OVERWRITE = False
AWS_S3_CUSTOM_DOMAIN = env.str('AWS_S3_CUSTOM_DOMAIN', '')
WS_S3_URL_PROTOCOL = env.str('AWS_S3_URL_PROTOCOL', 'https:')
AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')
AWS_S3_HOST = 's3-us-west-1.amazonaws.com'

# NOTE: Notify keys must be in a specfic format for the client to initialise,
# so using an invalid default here to prevent breakages locally / in tests
GOVNOTIFY_API_KEY = env.str(
    'GOVNOTIFY_API_KEY',
    'directory_cms_invalid-03185ee5-578c-4ffc-8774-2288e7b34e63-e82262ea-ae8c-4c6d-8570-c16afdc8347f' # noqa
)
GOVNOTIFY_REPLY_TO_EMAIL_ID = env.str('GOVNOTIFY_REPLY_TO_EMAIL_ID', '')
GOVNOTIFY_USER_PENDING_APPROVAL_TEMPLATE_ID = env.str('GOVNOTIFY_USER_PENDING_APPROVAL_TEMPLATE_ID', '')
GOVNOTIFY_USER_APPROVED_TEMPLATE_ID = env.str('GOVNOTIFY_USER_APPROVED_TEMPLATE_ID', '')


if env.bool('DEBUG_TOOLBAR_ON', False):

    INSTALLED_APPS += ['debug_toolbar']

    MIDDLEWARE = (
        ['debug_toolbar.middleware.DebugToolbarMiddleware'] +
        MIDDLEWARE
    )
    INTERNAL_IPS = ['127.0.0.1', '10.0.2.2']


# Business SSO API Client
DIRECTORY_SSO_API_CLIENT_BASE_URL = env.str('SSO_API_CLIENT_BASE_URL', '')
DIRECTORY_SSO_API_CLIENT_API_KEY = env.str('SSO_SIGNATURE_SECRET', '')
DIRECTORY_SSO_API_CLIENT_SENDER_ID = env.str('DIRECTORY_SSO_API_CLIENT_SENDER_ID', 'directory')
DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT = 15
SSO_PROXY_LOGOUT_URL = env.str('SSO_PROXY_LOGOUT_URL')
SSO_PROXY_SIGNUP_URL = env.str('SSO_PROXY_SIGNUP_URL')
SSO_PROXY_LOGIN_URL = env.str('SSO_PROXY_LOGIN_URL')
SSO_PROFILE_URL = ''
SSO_PROXY_PASSWORD_RESET_URL = env.str('SSO_PROXY_PASSWORD_RESET_URL')
SSO_PROXY_REDIRECT_FIELD_NAME = env.str('SSO_PROXY_REDIRECT_FIELD_NAME')
AUTH_USER_MODEL = 'sso.BusinessSSOUser'
AUTHENTICATION_BACKENDS = ['sso.backends.BusinessSSOUserBackend']
SSO_SESSION_COOKIE = env.str('SSO_SESSION_COOKIE')


if env.bool('ENFORCE_STAFF_SSO_ON', False):
    AUTHENTICATION_BACKENDS += [
        'django.contrib.auth.backends.ModelBackend',
        'authbroker_client.backends.AuthbrokerBackend'
    ]
    LOGIN_URL = reverse_lazy('authbroker_client:login')
    LOGIN_REDIRECT_URL = reverse_lazy('wagtailadmin_home')

    # authbroker config
    AUTHBROKER_URL = env.str('STAFF_SSO_AUTHBROKER_URL')
    AUTHBROKER_CLIENT_ID = env.str('AUTHBROKER_CLIENT_ID')
    AUTHBROKER_CLIENT_SECRET = env.str('AUTHBROKER_CLIENT_SECRET')

    MIDDLEWARE.append(
        'users.middleware.SSORedirectUsersToRequestAccessViews'
    )
    # Disable password management in Wagtail admin
    WAGTAIL_PASSWORD_MANAGEMENT_ENABLED = False
    WAGTAIL_PASSWORD_RESET_ENABLED = False
    WAGTAILUSERS_PASSWORD_ENABLED = False
    MIGRATE_EMAIL_USER_ON_LOGIN = env.bool('MIGRATE_EMAIL_USER_ON_LOGIN', False)
else:
    LOGIN_URL = '/admin/login/'


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}
