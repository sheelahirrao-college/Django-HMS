from rest_framework import serializers
from room.models import Room, Category


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['id', 'number', 'category', 'image', 'hotel', 'booked_from', 'booked_to', 'available', 'slug']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'hotel', 'slug']
