from django.contrib import admin
from .models import AgencyReview


class AgencyReviewAdmin(admin.ModelAdmin):
    # list_display = ('content_object.name',)
    pass


admin.site.register(AgencyReview, AgencyReviewAdmin)
