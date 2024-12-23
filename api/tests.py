from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.utils import timezone
from .models import Vehicle
import json

class VehicleAPITestCase(TestCase):

    def setUp(self):
        self.vehicle_data = {
            'vin': 10000000000000001,
            'stock_number': 1000000001,
            'status': 'ONS',
            'vehicle_type': 'NEW',
            'description': 'Brand new Toyota Vios',
            'price': 12000000.50,
            'photos_count': 5,
        }
        self.vehicle = Vehicle.objects.create(**self.vehicle_data)

        # Define URL endpoints
        self.create_vehicle = reverse('create-vehicle')
        self.update_vehicle_details = reverse('update-vehicle', kwargs={'vin': self.vehicle.vin})
        self.update_vehicle_status = reverse('sold-vehicle', kwargs={'vin': self.vehicle.vin})

    def test_create_Vehicle(self):
        # Test POST method to create a new Vehicle
        new_vehicle_data = {
            'VIN': 10000000000000002,
            'stock_number': 1000000002,
            'status': 'SLD',
            'vehicle_type': 'USED',
            'description': 'Used Toyota Innova',
            'price': 15500000.50,
            'photos_count': 8,
        }
        response = self.client.post(self.create_vehicle, new_vehicle_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_update_Vehicle(self):
        # Test PUT method to update an existing Vehicle
        updated_data = {
            'vin': 10000000000000004,
            'stock_number': 1000000004,
            'vehicle_type': 'USED',
            'description': 'Used Toyota Vios',
            'status': 'SLD',
            'price': 10200000.50,
            'photos_count': 9,
        }
        response = self.client.put(self.update_vehicle_details, updated_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_update_vehicle_status(self):
        # Test PATCH method to update an existing Vehicle
        updated_data = {
            'vin': 10000000000000004,
            'stock_number': 1000000004,
            'vehicle_type': 'USED',
            'description': 'Used Toyota Vios',
            'status': 'ONS',
            'price': 10200000.50,
            'photos_count': 9,
        }
        response = self.client.patch(self.update_vehicle_status, updated_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
