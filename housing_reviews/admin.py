from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

UserAdmin.list_display += ('date_joined',)
UserAdmin.list_filter += ('date_joined',)
# UserAdmin.fieldsets += ('created',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)