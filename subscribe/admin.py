from django.contrib import admin
from subscribe.models import Interested


class InterestedAdmin(admin.ModelAdmin):
	pass

admin.site.register(Interested, InterestedAdmin)
