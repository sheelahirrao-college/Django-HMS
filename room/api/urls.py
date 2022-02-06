from django.urls import path
from .views import (
    Room,
    Rooms,
    Category,
    Categories,
)
from django.conf import settings
from django.conf.urls.static import static

app_name = 'room'

urlpatterns = [
    path('roomapi/<slug>', Room.as_view(), name='room-api'),
    path('roomsapi', Rooms.as_view(), name='rooms-api'),
    path('categoryapi/<slug>', Category.as_view(), name='category-api'),
    path('categoriesapi', Categories.as_view(), name='categories-api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
