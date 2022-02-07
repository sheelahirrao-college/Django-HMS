from rest_framework import serializers
from booking.models import Booking
from room.models import Room


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['id', 'customer', 'hotel', 'room', 'booked_on', 'start_date', 'end_date', 'no_of_days', 'slug']


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['id', 'number', 'category', 'image', 'hotel', 'booked_from', 'booked_to', 'available', 'slug']


class RoomDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['id', 'category', 'image', 'hotel', 'slug']
