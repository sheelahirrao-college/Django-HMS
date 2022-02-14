from rest_framework import serializers
from room.models import Room, Category, RoomService


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['id', 'number', 'category', 'hotel', 'booked_from', 'booked_to', 'available', 'slug']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'hotel', 'slug']


class RoomServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomService
        fields = ['hotel', 'room', 'cleaning_required', 'description', 'slug']
