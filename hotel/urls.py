from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home', views.hotel_home, name='hotel-home'),
    path('login', views.hotel_login, name='hotel-login'),
    path('logout', views.hotel_logout, name='hotel-logout'),
    path('register', views.hotel_register, name='hotel-register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

