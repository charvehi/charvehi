"""
Django settings for xversion project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

#for register mail confirm
#gmail or google apps
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ramrana1912@gmail.com'
EMAIL_HOST_PASSWORD = 'mepassword'
EMAIL_PORT = 587

'''EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_HOST_USER = 'testsite_app'
EMAIL_HOST_PASSWORD = 'mys3cr3tp4ssw0rd'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'TestSite Team <noreply@example.com>'
'''
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
STATIC_DIR = os.path.join(BASE_DIR,'static')
MEDIA_DIR = os.path.join(BASE_DIR,'media')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lqhtthni$$_i#+e9xneu-qafg(0%$xf-s4=^2m9k(dujz6pu(='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'UserAccounts.apps.UseraccountsConfig',
    #added by ram for Usermodel 
    'booking.apps.BookingConfig',
    'dealer.apps.DealerConfig',
    'orders.apps.OrdersConfig',
    'review.apps.ReviewConfig',
    'voucher.apps.VoucherConfig',
    'localflavor',
    'pipeline',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'xversion.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'xversion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
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

WSGI_APPLICATION = 'xversion.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Charvehidb',
        'USER': 'root',
        'PASSWORD': 'ramjs',
        'HOST': '127.0.0.1',
        'PORT': '3307',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
#AUTH_USER_MODEL = 'uaccounts.UserProfileInfo'
AUTHENTICATION_BACKENDS = ('UserAccounts.backends.EmailPhoneBackend',)

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR, ]

MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'
#user authentication
#LOGOUT_REDIRECT_URL = '/useraccounts/login/'
AUTH_USER_MODEL = 'UserAccounts.User'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'useraccounts:home'

LOGIN_EXEMPT_URLS = {
    r'^accounts/logout/$',
    r'^accounts/register/$',
    r'^accounts/regdealer/$',

}
TIME_ZONE =  'Asia/Kolkata'
#end
CART_SESSION_ID = 'cart'
TIME_INPUT_FORMATS = [
    '%I:%M %p',  # 6:22:44 PM
    '%I:%M %p',  # 6:22 PM
    '%I %p',  # 6 PM
    '%H:%M',     # '14:30:59'
    '%H:%M.%f',  # '14:30:59.000200'
    '%H:%M',        # '14:30'
]
'''TIME_INPUT_FORMATS = [
    '%I:%M:%S %p',  # 6:22:44 PM
    '%I:%M %p',  # 6:22 PM
    '%I %p',  # 6 PM
    '%H:%M:%S',     # '14:30:59'
    '%H:%M:%S.%f',  # '14:30:59.000200'
    '%H:%M',        # '14:30'
]'''

# django-pipeline config
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.jsmin.JSMinCompressor'
PIPELINE_CSS_COMPRESSOR = 'mvp.plans.CSSMin.CSSCompressor'

PIPELINE = {
    'STYLESHEETS': {
        'index_direct': {
            'source_filenames': (
                'stylesheet/uaccounts/reg-log.css',
                'stylesheet/slider.css',
                'slick-1.8.1/slick/slick.css',
                'slick-1.8.1/slick/slick-theme.css',
                'frontpage/custom.css',
            ),
            'extra_context': {
                'media': 'screen',
            },
            'output_filename': 'stylesheet/index_direct.css',
        },
    },
    'JAVASCRIPT': {
        'nodal_serve': {
            'source_filenames': (
                'slick-1.8.1/slick/slick.min.js',
                'frontpage/js.js',
            ),
            'output_filename': 'js/nodal_serve.js',
        }
    }
}




