import os
import dj_database_url
from unipath import Path

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
    raise ImproperlyConfigured(error_msg)

PROJECT_DIR = Path(__file__).ancestor(3)

DEBUG = os.environ.get('DEBUG', False)
TEMPLATE_DEBUG = DEBUG

DATABASES = {"default": dj_database_url.config()}  # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = PROJECT_DIR.child('staticfiles')
STATIC_URL = '/static/'

SECRET_KEY = os.environ.get('SECRET_KEY')

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

ADMINS = (
    ('St Andrews Housing Reviews Team', 'hello@standrews-housing-reviews.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-uk'

SITE_ID = 2 if DEBUG else 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True




# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'housing_reviews.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'housing_reviews.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # root('templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',

    # allauth specific context processors
    # 'allauth.account.context_processors.account',
    # 'allauth.socialaccount.context_processors.socialaccount',
)

DJANGO_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    'gunicorn',
    'django_extensions',
    'model_utils',
    'djangosecure',
    'storages',
    'raven.contrib.django.raven_compat',
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'djangoratings',
    'django_activeurl',
    'analytical',
)

LOCAL_APPS = (
    'housing_reviews',
    'subscribe',
    'agencies',
    'reviews',
    'come_in',
)

INSTALLED_APPS = LOCAL_APPS + DJANGO_APPS + THIRD_PARTY_APPS


#   Heroku   #
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# END Heroku #

ALLOWED_HOSTS = '*'

SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True

# Crispy forms #
CRISPY_TEMPLATE_PACK = 'bootstrap'


def include_config(filename):
    filename = PROJECT_DIR.child('housing_reviews', 'settings', filename)
    with open(filename) as f:
        code = compile(f.read(), filename, 'exec')
        exec(code)

include_config('sentry.py')
include_config('logging.py')
include_config('email.py')
include_config('auth.py')
include_config('analytics.py')
include_config('mailchimp.py')
