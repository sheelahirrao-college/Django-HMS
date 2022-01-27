from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import RoomSerializer, CategorySerializer
from room.models import Room, Category


class RoomAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        room = Room.objects.filter(slug=slug)
        serializer = RoomSerializer(room, many=True)
        return Response(serializer.data)

    def post(self, request, slug):
        slug = 'newroom'
        room = Room()
        serializer = RoomSerializer(room, data=request.data)
        request.data['hotel'] = request.user.id
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self, request, slug):
        room = Room.objects.get(slug=slug)
        hotel = request.user
        room = Room()
        if room.hotel != hotel:
            return Response({
                'response': 'You do not have permission to edit this room'
            })
        serializer = RoomSerializer(room, data=request.data)
        request.data['hotel'] = request.user.id
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = "Room Updated Successfully"
            return Response(data=data)
        return Response(serializer.errors)

    def delete(self, request, slug):
        room = Room.objects.get(slug=slug)
        hotel = request.user
        if room.hotel != hotel:
            return Response({
                'response': 'You do not have permission to delete this room'
            })
        delete = room.delete()
        data = {}
        if delete:
            data['success'] = 'Room Successfully Deleted'
        else:
            data['failure'] = 'Room Delete Failed'
        return Response(data=data)


class RoomsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        room = Room.objects.filter(hotel=request.user.id)
        serializer = RoomSerializer(room, many=True)
        return Response(serializer.data)


class CategoryAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        category = Category.objects.filter(slug=slug)
        serializer = RoomSerializer(category, many=True)
        return Response(serializer.data)

    def post(self, request, slug):
        slug = 'newcategory'
        category = Category()
        serializer = RoomSerializer(category, data=request.data)
        request.data['hotel'] = request.user.id
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self, request, slug):
        category = Category.objects.get(slug=slug)
        hotel = request.user
        category = Category()
        if category.hotel != hotel:
            return Response({
                'response': 'You do not have permission to edit this category'
            })
        serializer = CategorySerializer(category, data=request.data)
        request.data['hotel'] = request.user.id
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = "Category Updated Successfully"
            return Response(data=data)
        return Response(serializer.errors)

    def delete(self, request, slug):
        category = Category.objects.get(slug=slug)
        hotel = request.user
        if category.hotel != hotel:
            return Response({
                'response': 'You do not have permission to delete this category'
            })
        delete = category.delete()
        data = {}
        if delete:
            data['success'] = 'Category Successfully Deleted'
        else:
            data['failure'] = 'Category Delete Failed'
        return Response(data=data)


class CategoriesAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        category = Category.objects.filter(hotel=request.user.id)
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
