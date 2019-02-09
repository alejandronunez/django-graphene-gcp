"""
Django settings for api project.
"""
import os
import datetime


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '24353453sdffffffffffffffffme%tallv6ow1('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'graphene_django',
    'corsheaders',
    'ads',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'api.urls'

WSGI_APPLICATION = 'api.wsgi.application'
GAE_SDK = True if os.getenv('SERVER_SOFTWARE', '').startswith('Development') else False

# If it is there in GAE
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):  # pragma: no cover
    # KEY_DICT = get_and_decrypt_keys()
    # # Database
    # # https://docs.djangoproject.com/en/1.11/ref/settings/#databases
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.mysql',
    #         'NAME': KEY_DICT['DB_NAME'],
    #         'USER': KEY_DICT['DB_USER'],
    #         'PASSWORD': KEY_DICT['DB_PASSWORD'],
    #         'HOST': KEY_DICT['DB_HOST'],
    #         'PORT': KEY_DICT['DB_PORT'],
    #     }
    # }
    pass

else:

    GAE_SDK_PATH = "%s/platform/google_appengine" % os.getenv('GAE_SDK_PATH', '')

    # Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'djangographene'),
            'USER': os.environ.get('DB_USER', 'superuser'),
            'PASSWORD': os.environ.get('DB_PASSWORD', '123123'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '3306'),
        }
    }

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Graphene settings
GRAPHENE = {
    'SCHEMA': 'api.root_schema.SCHEMA',  # Where your Graphene schema lives
    'SCHEMA_OUTPUT': 'data/schema.json',
    'MIDDLEWARE': [
        'graphene_django.debug.DjangoDebugMiddleware',
    ]
}

# Console Logging
LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler'
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'api': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'elasticsearch': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'graphql': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
