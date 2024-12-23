from django.shortcuts import get_object_or_404

# Create your views here.
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View

from .models import Vehicle, Statistics

from datetime import datetime
import json

def handle_invalid_json():
    return JsonResponse({'error': 'Invalid JSON format'}, status=400)

class VehicleView(View):
    def post(self, request, *args, **kwargs):
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body) 
            except json.JSONDecodeError: 
                return handle_invalid_json()
            vehicle_data = {k.lower(): v for k, v in data.items()}
            new_vehicle = Vehicle.objects.create(**vehicle_data)

            try:
                new_vehicle.full_clean()
            except ValidationError as e:
                return JsonResponse({'error': f'Invalid JSON format. {e}'}, status=400)

            new_vehicle.save()
            return JsonResponse({'message': 'Vehicle created'}, status=200)
        else:
            return handle_invalid_json()

    def put(self, request, vin):
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body) 
            except json.JSONDecodeError: 
                return handle_invalid_json()
            vehicle = get_object_or_404(Vehicle, vin=vin)
            for field, val in data.items():
                if val is not None and field != 'status':
                    setattr(vehicle, field, val)

            try:
                vehicle.full_clean()
            except ValidationError as e:
                return JsonResponse({'error': f'Invalid JSON format. {e}'}, status=400)
            
            vehicle.save()
            return JsonResponse({'message': 'Vehicle updated'}, status=200)
        else:
            return handle_invalid_json()
    
    def patch(self, request, vin):
        vehicle = get_object_or_404(Vehicle, vin=vin)
        setattr(vehicle, 'status', 'SLD')
        setattr(vehicle, 'end_date', datetime.now().date())

        vehicle.save()
        return JsonResponse({'message': 'Vehicle status updated'}, status=200)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({"error": "Method not allowed. Please use POST."}, status=405)
