from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .permissions import IsRoomManager
from .serializers import (
    RoomSerializer,
    CategorySerializer,
)

from room.models import Room, Category
from accounts.models import Hotel, RoomManager


class HotelRoom(APIView):

    permission_classes = [IsAuthenticated, IsRoomManager]

    def get(self, request, slug):
        try:
            room = Room.objects.get(slug=slug)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            room_manager = RoomManager.objects.get(user=request.user)
        except RoomManager.DoesNotExist:
            return Response({
                'response': 'Room Manager Object Not Created For This User'
            })

        try:
            hotel = Hotel.objects.get(name=room_manager.hotel)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if room.hotel != hotel:
            return Response({
                'response': 'The Room You Are Trying To View Does Not Belong To Your Hotel',
            })
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def post(self, request, slug):
        slug = 'newroom'

        try:
            room_manager = RoomManager.objects.get(user=request.user)
        except RoomManager.DoesNotExist:
            return Response({
                'response': 'Room Manager Object Not Created For This User'
            })

        try:
            hotel = Hotel.objects.get(name=room_manager.hotel)
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
            room_manager = RoomManager.objects.get(user=request.user)
        except RoomManager.DoesNotExist:
            return Response({
                'response': 'Room Manager Object Not Created For This User'
            })

        try:
            hotel = Hotel.objects.get(name=room_manager.hotel)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if room.hotel != hotel:
            return Response({
                'response': 'The Room You Are Trying To Edit Does Not Belong To Your Hotel',
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
            room_manager = RoomManager.objects.get(user=request.user)
        except RoomManager.DoesNotExist:
            return Response({
                'response': 'Room Manager Object Not Created For This User'
            })

        try:
            hotel = Hotel.objects.get(name=room_manager.hotel)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if room.hotel != hotel:
            return Response({
                'response': 'The Room You Are Trying To Delete Does Not Belong To Your Hotel',
            })

        delete = room.delete()
        data = {}
        if delete:
            data['success'] = 'Room Deleted Successfully'
        else:
            data['failure'] = 'Room Delete Failed'
        return Response(data=data)


class HotelRooms(APIView):

    def get(self, request):

        try:
            room_manager = RoomManager.objects.get(user=request.user)
        except RoomManager.DoesNotExist:
            return Response({
                'response': 'Room Manager Object Not Created For This User'
            })

        try:
            hotel = Hotel.objects.get(name=room_manager.hotel)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        room = Room.objects.filter(hotel=hotel)
        serializer = RoomSerializer(room, many=True)
        return Response(serializer.data)


class HotelRoomCategory(APIView):

    permission_classes = [IsAuthenticated, IsRoomManager]

    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            room_manager = RoomManager.objects.get(user=request.user)
        except RoomManager.DoesNotExist:
            return Response({
                'response': 'Room Manager Object Not Created For This User'
            })

        try:
            hotel = Hotel.objects.get(name=room_manager.hotel)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if category.hotel != hotel:
            return Response({
                'response': 'The Category You Are Trying To View Does Not Belong To Your Hotel',
            })

        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def post(self, request, slug):
        slug = 'newcategory'
        category = Category()

        try:
            room_manager = RoomManager.objects.get(user=request.user)
        except RoomManager.DoesNotExist:
            return Response({
                'response': 'Room Manager Object Not Created For This User'
            })

        try:
            hotel = Hotel.objects.get(name=room_manager.hotel)
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
            room_manager = RoomManager.objects.get(user=request.user)
        except RoomManager.DoesNotExist:
            return Response({
                'response': 'Room Manager Object Not Created For This User'
            })

        try:
            hotel = Hotel.objects.get(name=room_manager.hotel)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if category.hotel != hotel:
            return Response({
                'response': 'The Category You Are Trying To Edit Does Not Belong To Your Hotel',
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
            room_manager = RoomManager.objects.get(user=request.user)
        except RoomManager.DoesNotExist:
            return Response({
                'response': 'Room Manager Object Not Created For This User'
            })

        try:
            hotel = Hotel.objects.get(name=room_manager.hotel)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if category.hotel != hotel:
            return Response({
                'response': 'The Category You Are Trying To Delete Does Not Belong To Your Hotel',
            })

        delete = category.delete()
        data = {}
        if delete:
            data['success'] = 'Category Deleted Successfully'
        else:
            data['failure'] = 'Category Delete Failed'
        return Response(data=data)


class HotelRoomCategories(APIView):

    def get(self, request):

        try:
            room_manager = RoomManager.objects.get(user=request.user)
        except RoomManager.DoesNotExist:
            return Response({
                'response': 'Room Manager Object Not Created For This User'
            })

        try:
            hotel = Hotel.objects.get(name=room_manager.hotel)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        category = Category.objects.filter(hotel=hotel)
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
