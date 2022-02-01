from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import (
    RoomSerializer,
    CategorySerializer,
)
from room.models import Room, Category


class RoomAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        try:
            room = Room.objects.get(slug=slug)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        hotel = request.user
        if room.hotel != hotel:
            return Response({
                'response': 'You do not have permission to view this room',
            })
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def post(self, request, slug):
        slug = 'newroom'
        request.data._mutable = True
        request.data['hotel'] = request.user.id
        if request.data['booked_from'] is None and request.data['booked_to'] is None:
            request.data['available'] = True
        else:
            request.data['available'] = False
        request.data._mutable = False
        serializer = RoomSerializer(data=request.data, partial=True)

        category = Category.objects.filter(hotel=request.user.id).values('name')
        for c in category:
            if request.data['category'] != c['name']:
                return Response({
                    'response': 'Invalid Category',
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

        hotel = request.user
        if room.hotel != hotel:
            return Response({
                'response': 'You do not have permission to edit this room'
            })

        request.data._mutable = True
        request.data['hotel'] = request.user.id
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

        hotel = request.user
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


class RoomsAPIView(APIView):

    def get(self, request):
        room = Room.objects.filter(hotel=request.user.id)
        serializer = RoomSerializer(room, many=True)
        return Response(serializer.data)


class CategoryAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        hotel = request.user
        if category.hotel != hotel:
            return Response({
                'response': 'You do not have permission to view this category'
            })

        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def post(self, request, slug):
        slug = 'newcategory'
        category = Category()

        request.data._mutable = True
        request.data['hotel'] = request.user.id
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

        hotel = request.user
        if category.hotel != hotel:
            return Response({
                'response': 'You do not have permission to edit this category'
            })

        request.data._mutable = True
        request.data['hotel'] = request.user.id
        request.data['slug'] = request.user.id + request.data.number
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

        hotel = request.user
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


class CategoriesAPIView(APIView):

    def get(self, request):
        category = Category.objects.filter(hotel=request.user.id)
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
