from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import (
    RoomSerializer,
    CategorySerializer,
)
from room.models import Room, Category
from accounts.models import Hotel


class Room(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        try:
            room = Room.objects.get(slug=slug)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            hotel = Hotel.objects.get(user=request.user)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if room.hotel != hotel:
            return Response({
                'response': 'You do not have permission to view this room',
            })
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def post(self, request, slug):
        slug = 'newroom'

        try:
            hotel = Hotel.objects.get(user=request.user)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        request.data._mutable = True
        request.data['hotel'] = hotel.id
        if request.data['booked_from'] is None and request.data['booked_to'] is None:
            request.data['available'] = True
        else:
            request.data['available'] = False
        request.data._mutable = False
        serializer = RoomSerializer(data=request.data, partial=True)

        categories = Category.objects.filter(hotel=hotel).values('name')
        for c in categories:
            if request.data['category'] != c['name']:
                return Response({
                    'response': 'Invalid Category',
                    'category': c,
                })
            else:
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'response': 'Room Created Successfully',
                        'data': serializer.data,
                    })
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, slug):
        try:
            room = Room.objects.get(slug=slug)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            hotel = Hotel.objects.get(user=request.user)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if room.hotel != hotel:
            return Response({
                'response': 'You do not have permission to edit this room'
            })

        request.data._mutable = True
        request.data['hotel'] = hotel.id
        if request.data['booked_from'] is None and request.data['booked_to'] is None:
            request.data['available'] = True
        else:
            request.data['available'] = False
        request.data._mutable = False
        serializer = RoomSerializer(room, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = "Room Updated Successfully"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        try:
            room = Room.objects.get(slug=slug)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            hotel = Hotel.objects.get(user=request.user)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if room.hotel != hotel:
            return Response({
                'response': 'You do not have permission to delete this room'
            })

        delete = room.delete()
        data = {}
        if delete:
            data['success'] = 'Room Deleted Successfully'
        else:
            data['failure'] = 'Room Delete Failed'
        return Response(data=data)


class Rooms(APIView):

    def get(self, request):

        try:
            hotel = Hotel.objects.get(user=request.user)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        room = Room.objects.filter(hotel=hotel)
        serializer = RoomSerializer(room, many=True)
        return Response(serializer.data)


class Category(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            hotel = Hotel.objects.get(user=request.user)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if category.hotel != hotel:
            return Response({
                'response': 'You do not have permission to view this category'
            })

        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def post(self, request, slug):
        slug = 'newcategory'
        category = Category()

        try:
            hotel = Hotel.objects.get(user=request.user)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        request.data._mutable = True
        request.data['hotel'] = hotel.id
        request.data._mutable = False
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'response': 'Category Created Successfully',
                'data': serializer.data,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            hotel = Hotel.objects.get(user=request.user)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if category.hotel != hotel:
            return Response({
                'response': 'You do not have permission to edit this category'
            })

        request.data._mutable = True
        request.data['hotel'] = hotel.id
        request.data['slug'] = str(hotel.id) + request.data['name']
        request.data._mutable = False
        serializer = CategorySerializer(category, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = "Category Updated Successfully"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            hotel = Hotel.objects.get(user=request.user)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if category.hotel != hotel:
            return Response({
                'response': 'You do not have permission to delete this category'
            })

        delete = category.delete()
        data = {}
        if delete:
            data['success'] = 'Category Deleted Successfully'
        else:
            data['failure'] = 'Category Delete Failed'
        return Response(data=data)


class Categories(APIView):

    def get(self, request):

        try:
            hotel = Hotel.objects.get(user=request.user)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        category = Category.objects.filter(hotel=hotel)
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
