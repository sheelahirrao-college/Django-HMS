from django.urls import path
from .views import (
    HotelRoomService,
    HotelRoomServices,
    HotelRoom,
    HotelRooms,
    HotelRoomCategory,
    HotelRoomCategories,
)
from django.conf import settings
from django.conf.urls.static import static

app_name = 'room'

urlpatterns = [
    path('hotelroomservice/<slug>', HotelRoomService.as_view(), name='hotel-room-service-api'),
    path('hotelroomservices', HotelRoomServices.as_view(), name='hotel-room-services-api'),
    path('hotelroom/<slug>', HotelRoom.as_view(), name='hotel-room-api'),
    path('hotelrooms', HotelRooms.as_view(), name='hotel-rooms-api'),
    path('hotelcategory/<slug>', HotelRoomCategory.as_view(), name='hotel-category-api'),
    path('hotelcategories', HotelRoomCategories.as_view(), name='hotel-categories-api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
