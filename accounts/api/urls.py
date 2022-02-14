from django.urls import path
from .views import (
    UserRegistration,
    UserLogin,
    HotelProfile,
    CustomerProfile,
)

app_name = 'user'

urlpatterns = [
    path('customerprofile/<slug>', CustomerProfile.as_view(), name='customer-api'),
    path('hotelprofile/<slug>', HotelProfile.as_view(), name='user-api'),
    path('userregistration', UserRegistration.as_view(), name='user-registration-api'),
    path('userlogin', UserLogin.as_view(), name='user-login-api'),
]