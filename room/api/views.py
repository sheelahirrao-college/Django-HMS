from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .permissions import IsSuperUser, IsAdmin, IsStaff
from .serializers import (
    RoomSerializer,
    CategorySerializer,
)

from room.models import Room, Category
from accounts.models import Hotel


class HotelRoomCategory(APIView):

    permission_classes = [IsAuthenticated, IsSuperUser, IsAdmin, IsStaff]

    def get(self, request, slug):

        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            hotel = Hotel.objects.get(name=request.user.hotel)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.role != 1:
            return Response({
                'response': 'You Cannot View The Category Details - Only Room Managers Can Do That',
            })
        elif category.hotel != hotel:
            return Response({
                'response': 'The Category You Are Trying To View Does Not Belong To Your Hotel',
            })
        else:
            serializer = CategorySerializer(category)
            return Response(serializer.data)

    def post(self, request, slug):

        slug = 'newcategory'

        category = Category()

        if request.user.role != 1:
            return Response({
                'response': 'You Cannot Add A Category - Only Room Managers Can Do That',
            })
        else:
            try:
                hotel = Hotel.objects.get(name=request.user.hotel)
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
                    'category data': serializer.data,
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, slug):

        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            hotel = Hotel.objects.get(name=request.user.hotel)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.role != 1:
            return Response({
                'response': 'You Cannot Update The Category - Only Room Managers Can Do That',
            })
        elif category.hotel != hotel:
            return Response({
                'response': 'The Category You Are Trying To Edit Does Not Belong To Your Hotel',
            })
        else:
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
            hotel = Hotel.objects.get(name=request.user.hotel)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.role != 1:
            return Response({
                'response': 'You Cannot Delete The Category - Only Room Managers Can Do That',
            })
        elif category.hotel != hotel:
            return Response({
                'response': 'The Category You Are Trying To Delete Does Not Belong To Your Hotel',
            })
        else:
            delete = category.delete()
            data = {}
            if delete:
                data['success'] = 'Category Deleted Successfully'
            else:
                data['failure'] = 'Category Delete Failed'
            return Response(data=data)


class HotelRoomCategories(APIView):

    permission_classes = [IsAuthenticated, IsSuperUser, IsAdmin, IsStaff]

    def get(self, request):

        if request.user.role != 1:
            return Response({
                'response': 'You Cannot View Details Of The Categories - Only Room Managers Can Do That',
            })
        else:
            try:
                hotel = Hotel.objects.get(name=request.user.hotel)
            except Hotel.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            category = Category.objects.filter(hotel=hotel)
            serializer = CategorySerializer(category, many=True)
            return Response(serializer.data)


class HotelRoom(APIView):

    permission_classes = [IsAuthenticated, IsSuperUser, IsAdmin, IsStaff]

    def get(self, request, slug):

        try:
            room = Room.objects.get(slug=slug)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            hotel = Hotel.objects.get(name=request.user.hotel)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.role != 1:
            return Response({
                'response': 'You Cannot View The Room Details - Only Room Managers Can Do That',
            })
        elif room.hotel != hotel:
            return Response({
                'response': 'The Room You Are Trying To View Does Not Belong To Your Hotel',
            })
        else:
            serializer = RoomSerializer(room)
            return Response(serializer.data)

    def post(self, request, slug):

        slug = 'newroom'

        if request.user.role != 1:
            return Response({
                'response': 'You Cannot Add A Room - Only Room Managers Can Do That',
            })
        else:
            try:
                hotel = Hotel.objects.get(name=request.user.hotel)
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
                    pass
                else:
                    if serializer.is_valid():
                        serializer.save()
                        return Response({
                            'response': 'Room Created Successfully',
                            'room data': serializer.data,
                        })
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'response': 'Category Does Not Exist',
                'category': c['name'],
            })

    def put(self, request, slug):

        try:
            room = Room.objects.get(slug=slug)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            hotel = Hotel.objects.get(name=request.user.hotel)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.role != 1:
            return Response({
                'response': 'You Cannot Edit The Room Details - Only Room Managers Can Do That',
            })
        elif room.hotel != hotel:
            return Response({
                'response': 'The Room You Are Trying To Edit Does Not Belong To Your Hotel',
            })
        else:
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
            hotel = Hotel.objects.get(name=request.user.hotel)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.role != 1:
            return Response({
                'response': 'You Cannot Delete The Room - Only Room Managers Can Do That',
            })
        elif room.hotel != hotel:
            return Response({
                'response': 'The Room You Are Trying To Delete Does Not Belong To Your Hotel',
            })
        else:
            delete = room.delete()
            data = {}
            if delete:
                data['success'] = 'Room Deleted Successfully'
            else:
                data['failure'] = 'Room Delete Failed'
            return Response(data=data)


class HotelRooms(APIView):

    permission_classes = [IsAuthenticated, IsSuperUser, IsAdmin, IsStaff]

    def get(self, request):

        if request.user.role != 1:
            return Response({
                'response': 'You Cannot View Details Of The Rooms - Only Room Managers Can Do That',
            })
        else:
            try:
                hotel = Hotel.objects.get(name=request.user.hotel)
            except Hotel.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            room = Room.objects.filter(hotel=hotel)
            serializer = RoomSerializer(room, many=True)
            return Response(serializer.data)
