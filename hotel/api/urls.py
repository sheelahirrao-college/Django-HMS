from django.urls import path
from .views import (
    HotelRegistrationAPIView,
    HotelLoginAPIView,
)

app_name = 'hotel'

urlpatterns = [
    path('registerapi', HotelRegistrationAPIView.as_view(), name='hotel-register-api'),
    path('loginapi', HotelLoginAPIView.as_view(), name='hotel-login-api')
]