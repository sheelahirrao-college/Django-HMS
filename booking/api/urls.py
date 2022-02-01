from django.urls import path
from .views import Booking, RoomBooking

app_name = 'booking'

urlpatterns = [
    path('bookingapi', Booking.as_view(), name='booking-api'),
    path('roombookingapi/<slug>', RoomBooking.as_view(), name='room-booking-api'),
]
