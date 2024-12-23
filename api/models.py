from django.db import models
from django.core.exceptions import ValidationError

STATUS_CHOICES = ['ONS', 'SLD']
VEHICLE_TYPE_CHOICES = ['USED', 'NEW']
SOURCE_CHOICES = ['ABC', 'XYZ', 'QWE']

# Create your models here.
class Vehicle(models.Model):
    vin = models.CharField(max_length=17, unique=True)
    stock_number = models.CharField(max_length=10)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=3)
    vehicle_type = models.CharField(max_length=4)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    photos_count = models.IntegerField()

    def clean(self):
        # Validate the field explicitly
        if self.status not in STATUS_CHOICES:
            raise ValidationError({'error': 'Invalid status value. Allowed values are "ONS" or "SLD".'})
        
        if self.vehicle_type not in VEHICLE_TYPE_CHOICES:
            raise ValidationError({'error': 'Invalid vehicle_type value. Allowed values are "USED" or "NEW".'})


class Statistics(models.Model):
    date = models.DateField(auto_now_add=True)
    source = models.CharField(max_length=3)
    vdp = models.IntegerField()
    srp = models.IntegerField()
    vin = models.ForeignKey(Vehicle, to_field='vin', on_delete=models.CASCADE, related_name='stats')

    def clean(self):
        # Validate the field explicitly
        if self.source not in SOURCE_CHOICES:
            raise ValidationError({'error': 'Invalid source value. Allowed values are "ABC", "XYZ" or "QWE".'})
