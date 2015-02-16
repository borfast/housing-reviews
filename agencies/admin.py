from django.contrib import admin
from .models import Agency, Office


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'agency')

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     print "blasfe"
    #     if db_field.name == "main_office":
    #         kwargs["queryset"] = Office.objects.filter(agency__exact=request._obj_)

    #     return super(OfficeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class AgencyAdmin(admin.ModelAdmin):

    list_display = ('name', 'main_office')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "main_office":
            kwargs["queryset"] = Office.objects.filter(agency__exact=request._obj_)

        return super(AgencyAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference so we can access the object id later
        request._obj_ = obj
        return super(AgencyAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Agency, AgencyAdmin)
admin.site.register(Office, OfficeAdmin)
