from django.db import models
from djangoratings.fields import RatingField

class Agency(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(null=True, blank=True, upload_to="agencies_logos", height_field="logo_height", width_field="logo_width")
    logo_width = models.PositiveIntegerField(blank=True, null=True)
    logo_height = models.PositiveIntegerField(blank=True, null=True)
    website = models.CharField(blank=True, null=True, max_length=100)
    main_office = models.ForeignKey('Office', null=True, blank=True, related_name="main_office")
    rating = RatingField(range=5, can_change_vote=True, allow_anonymous=False) # 5 possible rating values, 1-5

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "agencies"


class Office(models.Model):
    agency = models.ForeignKey(Agency)
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    post_code = models.CharField(blank=True, null=True, max_length=100)

    def __unicode__(self):
        return self.name
