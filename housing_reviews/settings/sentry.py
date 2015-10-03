from .base import *

# Sentry
RAVEN_CONFIG = {
    'dsn': env('SENTRY_DSN')
}
