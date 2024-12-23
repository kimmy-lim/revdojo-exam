from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

def index(request):
    data = {'message': 'Welcome', 'status': 'success'}
    return JsonResponse(data, status=200)