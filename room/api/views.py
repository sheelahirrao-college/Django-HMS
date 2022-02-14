from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.utils.decorators import method_decorator
from .decorators import role_required, validate_room_manager
from .permissions import IsSuperUser, IsAdmin, IsStaff
from .serializers import (
    RoomSerializer,
    CategorySerializer,
    RoomServiceSerializer,
)

from room.models import Room, Category, RoomService
from accounts.models import Hotel


class HotelRoomCategory(APIView):

    permission_classes = [IsAuthenticated, IsSuperUser, IsAdmin, IsStaff]

    @method_decorator(role_required(allowed_roles=[1]))
    def get(self, request, slug):

        try:
            category = Category.objects.get(slug=slug, hotel=request.user.hotel)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category)
        return Response(serializer.data)

    @method_decorator(role_required(allowed_roles=[1]))
    def post(self, request, slug):

        slug = 'newcategory'

        category = Category()

        request.data._mutable = True
        request.data['hotel'] = request.user.hotel.id
        request.data._mutable = False
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'response': 'Category Created Successfully',
                'category data': serializer.data,
            })
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @method_decorator(role_required(allowed_roles=[1]))
    def put(self, request, slug):

        try:
            category = Category.objects.get(slug=slug, hotel=request.user.hotel)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        request.data._mutable = True
        request.data['hotel'] = request.user.hotel.id
        request.data['slug'] = str(request.data['hotel']) + request.data['name']
        request.data._mutable = False

        serializer = CategorySerializer(category, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = "Category Updated Successfully"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @method_decorator(role_required(allowed_roles=[1]))
    def delete(self, request, slug):

        try:
            category = Category.objects.get(slug=slug, hotel=request.user.hotel)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        delete = category.delete()
        data = {}
        if delete:
            data['success'] = 'Category Deleted Successfully'
        else:
            data['failure'] = 'Category Delete Failed'
        return Response(data=data)


class HotelRoomCategories(APIView):

    permission_classes = [IsAuthenticated, IsSuperUser, IsAdmin, IsStaff]

    @method_decorator(role_required(allowed_roles=[1]))
    def get(self, request):

        category = Category.objects.filter(hotel=request.user.hotel)
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)


class HotelRoom(APIView):

    permission_classes = [IsAuthenticated, IsSuperUser, IsAdmin, IsStaff]

    @method_decorator(role_required(allowed_roles=[1]))
    def get(self, request, slug):
        try:
            room = Room.objects.get(slug=slug, hotel=request.user.hotel)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RoomSerializer(room)
        return Response(serializer.data)

    @method_decorator(role_required(allowed_roles=[1]))
    def post(self, request, slug):

        slug = 'newroom'

        request.data._mutable = True
        request.data['hotel'] = request.user.hotel.id
        if request.data['booked_from'] is None and request.data['booked_to'] is None:
            request.data['available'] = True
        else:
            request.data['available'] = False
        request.data._mutable = False

        serializer = RoomSerializer(data=request.data, partial=True)

        categories = Category.objects.filter(hotel=request.user.hotel).values('name')
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
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response({
            'response': 'Category Does Not Exist',
            'category': c['name'],
        })

    @method_decorator(role_required(allowed_roles=[1]))
    def put(self, request, slug):

        try:
            room = Room.objects.get(slug=slug, hotel=request.user.hotel)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        request.data._mutable = True
        request.data['hotel'] = request.user.hotel.id
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
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @method_decorator(role_required(allowed_roles=[1]))
    def delete(self, request, slug):

        try:
            room = Room.objects.get(slug=slug, hotel=request.user.hotel)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        delete = room.delete()
        data = {}
        if delete:
            data['success'] = 'Room Deleted Successfully'
        else:
            data['failure'] = 'Room Delete Failed'
        return Response(data=data)


class HotelRooms(APIView):

    permission_classes = [IsAuthenticated, IsSuperUser, IsAdmin, IsStaff]

    @method_decorator(role_required(allowed_roles=[1]))
    def get(self, request):

        room = Room.objects.filter(hotel=request.user.hotel)
        serializer = RoomSerializer(room, many=True)
        return Response(serializer.data)


class HotelRoomService(APIView):

    permission_classes = [IsAuthenticated, IsSuperUser, IsAdmin, IsStaff]

    @method_decorator(role_required(allowed_roles=[1]))
    def get(self, request, slug):
        try:
            room_service = RoomService.objects.get(slug=slug, hotel=request.user.hotel)
        except RoomService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RoomServiceSerializer(room_service)
        return Response(serializer.data)

    @method_decorator(role_required(allowed_roles=[1]))
    def post(self, request, slug):

        slug = 'newroomservice'

        request.data._mutable = True
        request.data['hotel'] = request.user.hotel.id
        request.data._mutable = False

        serializer = RoomServiceSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'response': 'Room Service Generated Successfully',
                'room data': serializer.data,
            })
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @method_decorator(role_required(allowed_roles=[1]))
    def put(self, request, slug):

        try:
            room_service = RoomService.objects.get(slug=slug, hotel=request.user.hotel)
        except RoomService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        request.data._mutable = True
        request.data['hotel'] = request.user.hotel.id
        request.data._mutable = False

        serializer = RoomSerializer(room_service, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = "Room Service Updated Successfully"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @method_decorator(role_required(allowed_roles=[1]))
    def delete(self, request, slug):

        try:
            room_service = RoomService.objects.get(slug=slug, hotel=request.user.hotel)
        except RoomService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        delete = room_service.delete()
        data = {}
        if delete:
            data['success'] = 'Room Service Deleted Successfully'
        else:
            data['failure'] = 'Room Service Delete Failed'
        return Response(data=data)


class HotelRoomServices(APIView):

    permission_classes = [IsAuthenticated, IsSuperUser, IsAdmin, IsStaff]

    @method_decorator(role_required(allowed_roles=[1]))
    def get(self, request):

        room_services = RoomService.objects.filter(hotel=request.user.hotel)
        serializer = RoomSerializer(room_services, many=True)
        return Response(serializer.data)
