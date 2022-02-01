from django.urls import path
from .views import (
    RoomAPIView,
    RoomsAPIView,
    CategoryAPIView,
    CategoriesAPIView,
)
from django.conf import settings
from django.conf.urls.static import static

app_name = 'room'

urlpatterns = [
    path('roomapi/<slug>', RoomAPIView.as_view(), name='room-api'),
    path('roomsapi', RoomsAPIView.as_view(), name='rooms-api'),
    path('categoryapi/<slug>', CategoryAPIView.as_view(), name='category-api'),
    path('categoriesapi', CategoriesAPIView.as_view(), name='categories-api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
