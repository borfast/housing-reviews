from __future__ import absolute_import, unicode_literals

import environ


env = environ.Env(DEBUG=(bool, False),)  # set default values and casting

ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
APPS_DIR = ROOT_DIR.path('housing_reviews')

DEBUG = env('DEBUG')
TEMPLATE_DEBUG = DEBUG

# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
DATABASES = {"default": env.db()}

MEDIA_ROOT = str(ROOT_DIR('uploads'))
MEDIA_URL = ''
STATIC_ROOT = str(ROOT_DIR('staticfiles'))
STATIC_URL = '/static/'

SECRET_KEY = env('SECRET_KEY')

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
    str(APPS_DIR.path('static')),
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
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.google',
    'djangoratings',
    'django_activeurl',
    'analytical',
)

LOCAL_APPS = (
    'housing_reviews',
    'agencies',
    'reviews',
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
    filename = str(ROOT_DIR('housing_reviews', 'settings', filename))
    with open(filename) as f:
        code = compile(f.read(), filename, 'exec')
        exec code

include_config('logging.py')
include_config('email.py')
include_config('auth.py')
include_config('analytics.py')
include_config('mailchimp.py')
