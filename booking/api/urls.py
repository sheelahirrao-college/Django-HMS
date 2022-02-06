from django.urls import path
from .views import (
    BookRoom,
    AvailableRooms,
    RoomBookedStatus,
)

app_name = 'booking'

urlpatterns = [
    path('roombookedstatus/<slug>', RoomBookedStatus.as_view(), name='room-booked-status-api'),
    path('bookroomapi/<slug>', BookRoom.as_view(), name='book-room-api'),
    path('availableroomsapi', AvailableRooms.as_view(), name='available-rooms-api'),
]
