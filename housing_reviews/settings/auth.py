AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = 'reviews'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ALLOW_NEW_REGISTRATIONS = True

# django-come-in
ACCOUNT_INVITATION_DAYS = 30
INVITATIONS_PER_USER = 10
INVITE_MODE = True
CREATE_INVITE_USERS = False

# django-invitation and django-allauth integration
ACCOUNT_ADAPTER ="housing_reviews.accountadapter.AccountAdapter"
