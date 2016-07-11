"""
Django settings for bookocr project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG'))


LOGIN_URL = '/login/' # XXX
ALLOWED_HOSTS = [] # XXX


# Application definition

INSTALLED_APPS = [
	'bookshot.apps.BookshotConfig',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.humanize',
	'social.apps.django_app.default',
	'whitenoise.runserver_nostatic',
	'storages', # 
	# 'django_s3_storage',
]



MIDDLEWARE_CLASSES = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'whitenoise.middleware.WhiteNoiseMiddleware'
]


ROOT_URLCONF = 'bookocr.urls'

TEMPLATES = [
	{
	    'BACKEND': 'django.template.backends.django.DjangoTemplates',
	    'DIRS': [],
	    'APP_DIRS': True,
	    'OPTIONS': {
	        'debug': DEBUG,
	        'context_processors': [
	            'django.contrib.auth.context_processors.auth',
	            'django.contrib.messages.context_processors.messages',
	            'django.template.context_processors.debug',
	            'django.template.context_processors.request',
	            'django.template.context_processors.i18n',
	            'django.template.context_processors.media',
	            'django.template.context_processors.static',
	            'django.template.context_processors.tz',
	            'social.apps.django_app.context_processors.backends',
	            'social.apps.django_app.context_processors.login_redirect',
	        ],
	    },
	},
]

WSGI_APPLICATION = 'bookocr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
	'default': {
	    'ENGINE': 'django.db.backends.sqlite3',
	    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


AUTHENTICATION_BACKENDS = (
	'social.backends.facebook.FacebookOAuth2',
	'django.contrib.auth.backends.ModelBackend',
)

#
# social.apps.django_app settings
# https://github.com/omab/python-social-auth
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('FACEBOOK_SECRET')
 
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email, age_range'
}

# session serializer required by social app
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Internaxtionalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Seoul' #'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

INTERNAL_IPS = [
	'127.0.0.1',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
	os.path.join(PROJECT_ROOT, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


#
# django-storages settings
# from https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/
AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
    # 'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    # 'Cache-Control': 'max-age=94608000',
}

AWS_STORAGE_BUCKET_NAME = 'bookocr'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = 'ap-northeast-2' #"us-east-1"
AWS_S3_HOST = 's3-%s.amazonaws.com' % AWS_REGION
os.environ['S3_USE_SIGV4'] = 'True' # https://github.com/boto/boto/issues/2916

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

if not DEBUG:
	# This is used by the `static` template tag from `static`, if you're using that. Or if anything else
	# refers directly to STATIC_URL. So it's safest to always set it.
	# STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
	STATIC_URL = "https://%s/static/" % (AWS_S3_CUSTOM_DOMAIN, )

	# Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
	# you run `collectstatic`).
	# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
	STATICFILES_STORAGE = 's3_custom_storage.StaticStorage'


	#
	MEDIA_URL = "https://%s/media/" % (AWS_S3_CUSTOM_DOMAIN, )
	
	#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
	DEFAULT_FILE_STORAGE = 's3_custom_storage.MediaStorage'



# DEFAULT_FILE_STORAGE = "django_s3_storage.storage.S3Storage"
# STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"

# # The region to connect to when storing files.
# AWS_REGION = 'ap-northeast-2' #"us-east-1"

# # The S3 calling format to use to connect to the bucket.
# AWS_S3_CALLING_FORMAT = "boto.s3.connection.OrdinaryCallingFormat"

# # The host to connect to (only needed if you are using a non-AWS host)
# AWS_S3_HOST = ""

# # A prefix to add to the start of all uploaded files.
# AWS_S3_KEY_PREFIX = ""

# # Whether to enable querystring authentication for uploaded files.
# AWS_S3_BUCKET_AUTH = True

# # The expire time used to access uploaded files.
# AWS_S3_MAX_AGE_SECONDS = 60*60  # 1 hour.

# # A custom URL prefix to use for public-facing URLs for uploaded files.
# AWS_S3_PUBLIC_URL = ""

# # Whether to set the storage class of uploaded files to REDUCED_REDUNDANCY.
# AWS_S3_REDUCED_REDUNDANCY = False

# # A dictionary of additional metadata to set on the uploaded files.
# # If the value is a callable, it will be called with the path of the file on S3.
# AWS_S3_METADATA = {}

# # Whether to enable gzip compression for uploaded files.
# AWS_S3_GZIP = True

# # The S3 bucket used to store static files.
# AWS_S3_BUCKET_NAME_STATIC = ""

# # The S3 calling format to use to connect to the static bucket.
# AWS_S3_CALLING_FORMAT_STATIC = "boto.s3.connection.OrdinaryCallingFormat"

# # The host to connect to for static files (only needed if you are using a non-AWS host)
# AWS_S3_HOST_STATIC = ""

# # Whether to enable querystring authentication for static files.
# AWS_S3_BUCKET_AUTH_STATIC = False

# # A prefix to add to the start of all static files.
# AWS_S3_KEY_PREFIX_STATIC = ""

# # The expire time used to access static files.
# AWS_S3_MAX_AGE_SECONDS_STATIC = 60*60*24*365  # 1 year.

# # A custom URL prefix to use for public-facing URLs for static files.
# AWS_S3_PUBLIC_URL_STATIC = ""

# # Whether to set the storage class of static files to REDUCED_REDUNDANCY.
# AWS_S3_REDUCED_REDUNDANCY_STATIC = False

# # A dictionary of additional metadata to set on the static files.
# # If the value is a callable, it will be called with the path of the file on S3.
# AWS_S3_METADATA_STATIC = {}

# # Whether to enable gzip compression for static files.
# AWS_S3_GZIP_STATIC = True

#
# Test specific
#


TEST_RUNNER = 'bookocr.test.runner.BookOCRTestRunner' # 'django.test.runner.DiscoverRunner'

