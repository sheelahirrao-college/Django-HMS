from django.urls import path
from .views import (
    BookRoom,
    BookedRoomStatus,
    CustomerBookings,
)

app_name = 'booking'

urlpatterns = [
    path('customerbookings/<slug>', CustomerBookings.as_view(), name='customer-bookings-api'),
    path('roombookedstatus/<slug>', BookedRoomStatus.as_view(), name='room-booked-status-api'),
    path('bookroom/<slug>', BookRoom.as_view(), name='book-room-api'),
]
