from .base import get_env_variable

# Email settings
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = get_env_variable('EMAIL_HOST')
EMAIL_PORT = get_env_variable('EMAIL_PORT')
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = get_env_variable('DEFAULT_FROM_EMAIL')
EMAIL_USE_TLS = True
