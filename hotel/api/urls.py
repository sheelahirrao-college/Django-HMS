from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'hotel'

urlpatterns = [
    path('registerapi', views.hotel_registration_api_view, name='hotel-register-api'),
    path('loginapi', obtain_auth_token, name='hotel-login-api')
]