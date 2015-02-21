from django.db import models

from geopy.geocoders import GoogleV3

from locations.choices import STATE_CHOICES, COUNTRY_CHOICES
from locations.utils import unique_slugify


class Location(models.Model):
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250, choices=STATE_CHOICES, blank=True, help_text="State is not required if you are out of the country.")
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, blank=True)
    latitude = models.CharField(max_length=250, blank=True, editable=False)
    longitude = models.CharField(max_length=250, blank=True, editable=False)
    slug = models.SlugField(editable=False)
    default_location = models.BooleanField(default=False)

    def __unicode__(self):
        if self.state:
            return "%s, %s" % (self.city, self.state)
        else:
            return "%s, %s" % (self.city, self.country)

    def save(self, *args, **kwargs):
        slug_title = self.city + self.country
        unique_slugify(self, slug_title)
        geolocator = GoogleV3()
        location = "%s %s %s" % (self.city, self.state, self.country)
        address, (latitude, longitude) = geolocator.geocode(location)

        self.latitude = latitude
        self.longitude = longitude
        super(Location, self).save(*args, **kwargs)
