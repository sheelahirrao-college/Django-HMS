from django.urls import path
from .views import (
    UserRegistration,
    UserLogin,
    HotelProfile,
    RoomManagerProfile,
    CustomerProfile,
    HotelRegistration,
)

app_name = 'hotel'

urlpatterns = [
    path('hotelregistrationapi', HotelRegistration.as_view(), name='hotel-registration-api'),
    path('customerapi', CustomerProfile.as_view(), name='customer-api'),
    path('roommanagerapi', RoomManagerProfile.as_view(), name='room-manager-api'),
    path('hotelapi', HotelProfile.as_view(), name='hotel-api'),
    path('userregistrationapi', UserRegistration.as_view(), name='user-registration-api'),
    path('userloginapi', UserLogin.as_view(), name='user-login-api'),
]