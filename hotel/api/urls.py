from django.urls import path
from .views import (
    HotelRegistrationAPIView,
    HotelLoginView,
)

app_name = 'hotel'

urlpatterns = [
    path('registerapi', HotelRegistrationAPIView.as_view(), name='hotel-register-api'),
    path('loginapi', HotelLoginView.as_view(), name='hotel-login-api')
]