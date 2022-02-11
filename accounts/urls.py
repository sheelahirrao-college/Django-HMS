from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home', views.user_home, name='user-home'),
    path('login', views.user_login, name='user-login'),
    path('logout', views.user_logout, name='user-logout'),
    path('register', views.user_register, name='user-register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

