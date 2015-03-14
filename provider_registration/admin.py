from django.contrib import admin
from provider_registration.models import RegistrationInfo


class RegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['provider_short_name', 'provider_long_name', 'base_url', 'property_list', 'approved_sets']}),
        ('Date information', {'fields': ['registration_date'], 'classes': ['collapse']})
    ]

    list_display = ('provider_short_name', 'provider_long_name', 'registration_date', 'was_registered_recently')
    list_filter = ['registration_date']
    search_fields = ['provider_long_name']

admin.site.register(RegistrationInfo, RegistrationAdmin)
