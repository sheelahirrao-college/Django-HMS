from rest_framework import serializers
from room.models import Room, Category


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['number', 'type', 'image', 'hotel']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'hotel']
