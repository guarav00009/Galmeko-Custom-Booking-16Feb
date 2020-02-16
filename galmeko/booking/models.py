from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
User = settings.AUTH_USER_MODEL
from setting.models import Vehicle,VehicleCategory,Features
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import *

# Create your models here.
class Booking(models.Model):
    STATUS_CHOICES = (
    ('', 'Please Select User'),
    ('1', 'Hospital'),
    ('3', 'User'), 
    ) 
    booking_type = models.CharField(
    _('Booking Type'), choices=STATUS_CHOICES, max_length=50)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    origin_name = models.CharField(_('Name'),max_length=40, blank=False, null=False)
    origin_phone = models.CharField(_('Phone'),max_length=40, blank=False, null=False)
    origin_address = models.CharField(_('Address'),max_length=200, blank=False, null=False)
    origin_geocode = models.CharField(_('Origin Cordinate'), max_length=30,blank=True, null=True)
    destination_name = models.CharField(_('Name'),max_length=40, blank=False, null=False)
    destination_phone = models.CharField(_('Phone'),max_length=40, blank=False, null=False)
    destination_address = models.CharField(_('Address'),max_length=200, blank=False, null=False)
    destination_geocode = models.CharField(_('Destination Cordinate'), max_length=30,blank=True, null=True)
    booking_msg = models.TextField(_('Notes'),blank=True)
    round_trip = models.BooleanField(default=False)
    category = models.ForeignKey(VehicleCategory, on_delete=models.CASCADE, blank=True, null=True)
    STATUS_CHOICES = (
    (1, 'Active'),
    (2, 'Pending'),
    (3, 'Cancel'),
    (4, 'Delete'),
    ) 
    status = models.IntegerField(
    _('Status'), choices=STATUS_CHOICES,default=1)
    time = models.DateTimeField(auto_now_add=True)
    fare = models.DecimalField(_(u'Fare'), decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))])
    date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "bookings"
        verbose_name = 'Bookings'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return self.booking_type


class BookingStop(models.Model):
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE ,null=False,blank=False)
    name = models.CharField(max_length=25, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    stop_geocode = models.CharField(_('Stop Cordinate'), max_length=30,blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "booking_stops"
        verbose_name = 'Stops'
        verbose_name_plural = 'Stops'

    def __str__(self):
        return self.name

class BookingFeature(models.Model):
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE ,null=False,blank=False)
    feature = models.ForeignKey(Features,on_delete=models.CASCADE ,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "booking_features"
        verbose_name = 'Booking Features'
        verbose_name_plural = 'Booking Features'

    def __unicode__(self):
        return self.feature