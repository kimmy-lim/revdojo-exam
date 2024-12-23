# myapp/urls.py
from django.urls import path
from . import views  # Import views from your app

urlpatterns = [
    path('vehicle', views.VehicleView.as_view(), name='create-vehicle'),
    path('vehicle/<int:vin>', views.VehicleView.as_view(), name='update-vehicle'),
    path('vehicle/<int:vin>/sold', views.VehicleView.as_view(), name='sold-vehicle'),
    path('vehicle/statistics', views.VehicleStatisticsView.as_view(), name='vehicle-statistics'),

]
