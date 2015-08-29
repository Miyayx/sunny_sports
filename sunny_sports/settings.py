#-*- coding:utf-8 -*-
"""
Django settings for sunny_sports project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
#os.environ['HTTPS'] = "on"
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
import platform
OS = platform.dist()[0]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x*7jb4_74q_pf6s05%@7ecrt*fhxp5s&3p%xer$)mw4x#xj+j)'

# SECURITY WARNING: don't run with debug turned on in production!
if OS == 'centos' and 'nginx' in os.getcwd():
    DEBUG = False
    TEMPLATE_DEBUG = False
    ALLOWED_HOSTS = ['localhost','127.0.0.1','121.52.209.117','kuaileticao.com','www.kuaileticao.com', 'kuaileticao.miyayx.me', 'test.kuaileticao.com']
else:
    DEBUG = True
    TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = ['*']
print os.getcwd()
print "DEBUG?",DEBUG

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'captcha',
    #'corsheaders',
    'kombu.transport.django',
    'sp',
    'payment',
    'student',
    'game',
    'group',
    'club',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    #CorsMiddleware needs to come before Django's CommonMiddleware if you are using Django's USE_ETAGS = True setting, otherwise the CORS headers will be lost from the 304 not-modified responses, causing errors in some browsers.
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'sp.middleware.AutoLogout',
)

import djcelery
djcelery.setup_loader()
#BROKER_URL = 'django://'
#BROKER_URL = 'amqp://'
#BROKER_HOST = "localhost"
#BROKER_HOST = "121.52.209.117"
#BROKER_PORT = 5672
#BROKER_USER = "kltc"
#BROKER_PASSWORD = "queen-dorm"
#BROKER_VHOST = "/"
BROKER_URL = 'amqp://kltc:queen-dorm@121.52.209.117:5672/kltc'
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"


#Handle session is not Json Serializable
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
# Auto logout delay in minutes
AUTO_LOGOUT_DELAY = 60 #equivalent to 60 minutes

ROOT_URLCONF = 'sunny_sports.urls'

WSGI_APPLICATION = 'sunny_sports.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'STORAGE_ENGINE': 'MyISAM / INNODB / ETC',
        'ENGINE': 'django.db.backends.mysql',
        #'ENGINE': 'mysql.connector.django',
        'NAME': 'sunny_sports' if DEBUG else 'kuaileticao',
        #'NAME': 'kuaileticao',
        #'USER': 'root',
        #'PASSWORD': '123',
        #'HOST': '127.0.0.1',
        'USER': 'queen',
        'PASSWORD': 'dorm',
        #'HOST': '104.236.146.204',
        'HOST': '121.52.209.117',
        'PORT': '3306',
        'OPTIONS': {
            'use_unicode': True, 
            'charset': 'utf8',
            'init_command': 'SET '
                 'storage_engine=INNODB,'
                 'character_set_connection=utf8,'
                 'collation_connection=utf8_bin'
            },
    }
}

print "DATABASE:",DATABASES['default']['NAME']

DATE_FORMAT = "Y-m-d"
DATETIME_FORMAT = "Y-m-d H:i"

AUTH_USER_MODEL = 'sp.MyUser'     
AUTHENTICATION_BACKENDS = ( 'sp.backend.MyBackend', )

LOGIN_URL='/'
LOGOUT_URL='/login'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

LANGUAGE=(
        ('zh-cn', u'简体中文'), # instead of 'zh-CN'
        ('zh-tw', u'繁體中文'), # instead of 'zh-TW'
        )

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Template files(HTML)
TEMPLATE_DIRS=( 
        os.path.join(BASE_DIR, 'templates').replace('\\','/'), 
        os.path.join(BASE_DIR, '/payment/templates').replace('\\','/'), 
        ) 

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_DIRS=( 
        os.path.join(BASE_DIR, 'static').replace('\\','/'), 
        ) 


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\','/')

PHOTO_URL = '/photo/'
PHOTO_ROOT = 'http://7xjdtv.com1.z0.glb.clouddn.com/'
DEFAULT_PHOTO = 'upload/default00.jpg'

# Role definition
USER_ROLES = (
        'centre',
        'coach_org',
        'student',
        'coach',
        'club',
        'team',
        'committee',
        )

CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_dots',)
MSG_CODE = True if OS == 'centos' else False
IGNORE_PHONE=["13812345678","13712345678","15110099952"]

CORS_ORIGIN_ALLOW_ALL = True

HOST = 'kuaileticao.miyayx.me' if DEBUG else 'kuaileticao.com'
print 'HOST:',HOST

import datetime
#PAYMENT_LIMIT=datetime.timedelta(days=1)
PAYMENT_LIMIT=datetime.timedelta(minutes=1)

