from django.shortcuts import get_object_or_404

# Create your views here.
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View
from django.db.models import Sum

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
        ignore_field = ['status', 'vin']
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body) 
            except json.JSONDecodeError: 
                return handle_invalid_json()
            vehicle = get_object_or_404(Vehicle, vin=vin)
            for field, val in data.items():
                if val is not None and field.lower() not in ignore_field:
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

class VehicleStatisticsView(View):
    def post(self, request, *args, **kwargs):
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body) 
            except json.JSONDecodeError: 
                return handle_invalid_json()
            
            data = {k.lower(): v for k, v in data.items()}
            if 'vin' not in data:
                return JsonResponse({'error': f'Invalid JSON format. VIN field is required.'}, status=400)
            
            vehicle = get_object_or_404(Vehicle, vin=data['vin'])
            data['vin'] = vehicle
            new_statistic = Statistics.objects.create(**data)

            try:
                new_statistic.full_clean()
            except ValidationError as e:
                return JsonResponse({'error': f'Invalid JSON format. {e}'}, status=400)

            new_statistic.save()
            return JsonResponse({'message': 'Vehicle statistics created'}, status=200)
        else:
            return handle_invalid_json()
    
    def get(self, request):
        vin = request.GET.get('vin', None)
        stock_number = request.GET.get('stock_number', None)
        vehicle_type = request.GET.get('vehicle_type', None)
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        source = request.GET.get('source', None)

        vehicles = Vehicle.objects.filter(status='ONS')
        if vin:
            vehicles = vehicles.filter(vin=vin)
        if stock_number:
            vehicles = vehicles.filter(stock_number=stock_number)
        if vehicle_type:
            vehicles = vehicles.filter(vehicle_type=vehicle_type)
        
        data = []
        for vehicle in vehicles:
            statistics = vehicle.stats.all()
            if source:
                statistics = statistics.filter(source=source)
            if start_date:
                try:
                    datetime.strptime(start_date, '%Y-%m-%d')
                    statistics = statistics.filter(date__gte=start_date)
                except ValueError as e:
                    return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=200)
            if end_date:
                try:
                    datetime.strptime(end_date, '%Y-%m-%d')
                    statistics = statistics.filter(date__lte=end_date)
                except ValueError as e:
                    return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=200)
            
            sources = statistics.values_list('source', flat=True).distinct()
            for s in sources:
                subset_stat = statistics.filter(source=s)
                total_vdp = subset_stat.aggregate(total_vdp=Sum('vdp'))['total_vdp'] or 0
                total_srp = subset_stat.aggregate(total_srp=Sum('srp'))['total_srp'] or 0
                data.append({'VIN': vehicle.vin, 'Stock Number': vehicle.stock_number, 'Start Date': vehicle.start_date, \
                          'Vehicle Type': vehicle.vehicle_type, 'Description': vehicle.description, \
                           'Price': vehicle.price, 'Photos Count': vehicle.photos_count,\
                            'Total VDP Count': total_vdp, 'Total SRP Count': total_srp, 'Source':s})
        response = {'data': data}
        return JsonResponse(response, status=200)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({"error": "Method not allowed. Please use POST."}, status=405)