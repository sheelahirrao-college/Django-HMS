from django.urls import path
from .views import (
    HotelRegistrationAPIView,
    HotelLoginView,
    RoomManagerRegistrationAPIView,
    RoomManagerLoginView,
    CustomerRegistrationAPIView,
    CustomerLoginView,
)

app_name = 'hotel'

urlpatterns = [
    path('hotelregisterapi', HotelRegistrationAPIView.as_view(), name='hotel-register-api'),
    path('hotelloginapi', HotelLoginView.as_view(), name='hotel-login-api'),
    path('roommanagerregisterapi', RoomManagerRegistrationAPIView.as_view(), name='roommanager-register-api'),
    path('roommanagerloginapi', RoomManagerLoginView.as_view(), name='roommanager-login-api'),
    path('customerregisterapi', CustomerRegistrationAPIView.as_view(), name='customer-register-api'),
    path('customerloginapi', CustomerLoginView.as_view(), name='customer-login-api'),
]