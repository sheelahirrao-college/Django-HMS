from django.urls import path
from .views import (
    UserRegistration,
    UserLogin,
    Hotel,
    RoomManager,
    Customer,
    HotelRegistration,
)

app_name = 'hotel'

urlpatterns = [
    path('hotelregistrationapi', HotelRegistration.as_view(), name='hotel-registration-api'),
    path('customerapi', Customer.as_view(), name='customer-api'),
    path('roommanagerapi', RoomManager.as_view(), name='room-manager-api'),
    path('hotelapi', Hotel.as_view(), name='hotel-api'),
    path('userregistrationapi', UserRegistration.as_view(), name='user-registration-api'),
    path('userloginapi', UserLogin.as_view(), name='user-login-api'),
]