from django.db import models

STATUS_CHOICES = [('ONS', 'ONS'), ('SLD', 'SLD')]
VEHICLE_TYPE_CHOICES = [('USED', 'USED'), ('NEW', 'NEW')]
SOURCE_CHOICES = [('ABC', 'ABC'), ('XYZ', 'XYZ'), ('QWE', 'QWE')]

# Create your models here.
class Vehicle(models.Model):
    vin = models.CharField(max_length=17, unique=True)
    stock_number = models.CharField(max_length=10)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)
    vehicle_type = models.CharField(max_length=4, choices=VEHICLE_TYPE_CHOICES)
    description = models.TextField()
    price = models.FloatField()
    photos_count = models.IntegerField()

class Statistics(models.Model):
    date = models.DateField(auto_now_add=True)
    source = models.CharField(max_length=3, choices=SOURCE_CHOICES)
    vdp = models.IntegerField()
    srp = models.IntegerField()
    vin = models.ForeignKey(Vehicle, to_field='vin', on_delete=models.CASCADE, related_name='stats')
