from .base import *

DEBUG = True

INSTALLED_APPS += ("debug_toolbar", )

# For Django Debug Toolbar
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TEMPLATE_CONTEXT': True,
}

MIDDLEWARE_CLASSES += ("debug_toolbar.middleware.DebugToolbarMiddleware", )