from django.urls import path
from .views import (
    BookRoom,
    AvailableRooms,
    RoomBookedStatus,
    CustomerBookings,
    CustomerBooking,
)

app_name = 'booking'

urlpatterns = [
    path('customerbooking/<slug>', CustomerBooking.as_view(), name='customer-booking-api'),
    path('customerbookings', CustomerBookings.as_view(), name='customer-bookings-api'),
    path('roombookedstatus/<slug>', RoomBookedStatus.as_view(), name='room-booked-status-api'),
    path('bookroom/<slug>', BookRoom.as_view(), name='book-room-api'),
    path('availablerooms', AvailableRooms.as_view(), name='available-rooms-api'),
]
