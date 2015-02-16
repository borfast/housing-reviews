from .base import get_env_variable

# Mailchimp settings
MAILCHIMP_API_KEY = get_env_variable('MAILCHIMP_API_KEY')
MAILCHIMP_INVITED_LIST_ID = get_env_variable('MAILCHIMP_INVITED_LIST_ID')
