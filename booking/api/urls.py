from django.urls import path
from .views import (
    BookRoom,
    AvailableRooms,
)

app_name = 'booking'

urlpatterns = [
    path('bookroomapi/<slug>', BookRoom.as_view(), name='book-room-api'),
    path('availableroomsapi', AvailableRooms.as_view(), name='available-rooms-api'),
]
