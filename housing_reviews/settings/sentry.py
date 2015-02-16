from .base import get_env_variable

# Sentry
RAVEN_CONFIG = {
    'dsn': get_env_variable('SENTRY_DSN')
}
