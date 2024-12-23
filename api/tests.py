from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from .models import Vehicle, Statistics
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

        self.vehicle_stats_data = {
            'vin': self.vehicle,
            'source': 'ABC',
            'vdp': 10,
            'srp': 20,
        }
        self.statistics = Statistics.objects.create(**self.vehicle_stats_data)

        self.vehicle_stats_data = {
            'vin': self.vehicle,
            'source': 'ABC',
            'vdp': 110,
            'srp': 220,
        }
        Statistics.objects.create(**self.vehicle_stats_data)

        self.vehicle_stats_data = {
            'vin': self.vehicle,
            'source': 'XYZ',
            'vdp': 300,
            'srp': 150,
        }
        Statistics.objects.create(**self.vehicle_stats_data)
        
        # Define URL endpoints
        self.create_vehicle = reverse('create-vehicle')
        self.update_vehicle_details = reverse('update-vehicle', kwargs={'vin': self.vehicle.vin})
        self.update_vehicle_status = reverse('sold-vehicle', kwargs={'vin': self.vehicle.vin})
        self.create_vehicle_statistics = reverse('vehicle-statistics')
        self.vehicle_details = reverse('vehicle-statistics')

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
        print(response.json())
        self.assertEqual(response.status_code, 200)

    def test_update_vehicle(self):
        # Test PUT method to update an existing Vehicle
        updated_data = {
            'vin': 10000000000000001,
            'stock_number': 1000000004,
            'vehicle_type': 'USED',
            'description': 'Used Toyota Vios',
            'status': 'SLD',
            'price': 10200000.50,
            'photos_count': 9,
        }
        response = self.client.put(self.update_vehicle_details, updated_data, content_type='application/json')
        print(response.json())
        self.assertEqual(response.status_code, 200)
    
    def test_update_vehicle_status(self):
        # Test PATCH method to update an existing Vehicle
        updated_data = {
            'vin': 10000000000000001,
            'stock_number': 1000000004,
            'vehicle_type': 'USED',
            'description': 'Used Toyota Vios',
            'status': 'ONS',
            'price': 10200000.50,
            'photos_count': 9,
        }
        response = self.client.patch(self.update_vehicle_status, updated_data, content_type='application/json')
        print(response.json())
        self.assertEqual(response.status_code, 200)

    def test_create_vehicle_statistic(self):
        new_stats_data = {
            'vin': 10000000000000001,
            'source': 'XYZ',
            'vdp': 30,
            'srp': 205,
        }
        response = self.client.post(self.create_vehicle_statistics, new_stats_data, content_type='application/json')
        print(response.json())
        self.assertEqual(response.status_code, 200)

    def test_filter_by_vehicle_vin(self):
        response = self.client.get(self.vehicle_details, {'vin': 10000000000000001})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['data'][0]['VIN'], '10000000000000001')
    
    def test_filter_by_stock_number(self):
        response = self.client.get(self.vehicle_details, {'stock_number': 1000000001})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['data'][0]['Stock Number'], '1000000001')
    
    def test_filter_by_source(self):
        response = self.client.get(self.vehicle_details, {'source': 'ABC'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['data'][0]['Source'], 'ABC')
    
    def test_filter_by_vehicle_type(self):
        response = self.client.get(self.vehicle_details, {'vehicle_type': 'NEW'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['data'][0]['Vehicle Type'], 'NEW')
    
    def test_filter_with_start_date(self):
        response = self.client.get(self.vehicle_details, {'start_date': '2024-12-24'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
    
    def test_filter_with_end_date(self):
        response = self.client.get(self.vehicle_details, {'end_date': '2024-12-24'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
    
    def test_filter_by_date_range(self):
        response = self.client.get(self.vehicle_details, {'start_date': '2024-12-24', 'end_date': '2024-12-24'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
    
    def test_combined_filter(self):
        filters = {'vin': 10000000000000001, 'source': 'ABC', 'vehicle_type': 'NEW', 
                   'start_date': '2024-12-24', 'end_date': '2024-12-24'}
        response = self.client.get(self.vehicle_details, filters)
        self.assertEqual(response.status_code, 200)
        data = response.json()
    