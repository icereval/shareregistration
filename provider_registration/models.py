import datetime

from django.db import models
from django.utils import timezone


class RegistrationInfo(models.Model):

    # Basic Information
    base_url = models.URLField()
    description = models.TextField()
    contact_email = models.EmailField()
    contact_name = models.CharField(max_length=100)
    oai_provider = models.BooleanField(default=False)
    provider_short_name = models.CharField(max_length=50)
    provider_long_name = models.CharField(max_length=100)
    link = 'Edit'

    # Terms of Service and Metadata Permissions Questions
    meta_tos = models.BooleanField(default=False)
    meta_license = models.CharField(max_length=100)
    meta_privacy = models.BooleanField(default=False)
    meta_sharing_tos = models.BooleanField(default=False)
    meta_license_extended = models.BooleanField(default=False)
    meta_future_license = models.BooleanField(default=False)

    # OAI Harvester Information
    property_list = models.TextField()
    approved_sets = models.TextField()
    registration_date = models.DateTimeField('date registered')

    def __unicode__(self):
        return self.provider_long_name

    def was_registered_recently(self, days=1):
        now = timezone.now()
        return now - datetime.timedelta(days) <= self.registration_date <= now

    was_registered_recently.admin_order_field = 'registration_date'
    was_registered_recently.boolean = True
    was_registered_recently.short_description = 'Registered recently?'
