from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import RoomSerializer

from room.models import Room
from hotel.models import Hotel


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def room_detail_api_view(request, slug):
    room = Room.objects.filter(slug=slug)
    serializer = RoomSerializer(room, many=True)
    return Response(serializer.data)


@api_view(['Put',])
@permission_classes((IsAuthenticated,))
def room_update_api_view(request, slug):
    room = Room.objects.get(slug=slug)

    hotel = request.user
    room = Room(hotel=hotel)
    if room.hotel != hotel:
        return Response({'response': 'You do not have permission to edit that'})

    serializer = RoomSerializer(room, data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data['success'] = "Update Successful"
        return Response(data=data)
    return Response(serializer.errors)


@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def room_delete_api_view(request, slug):
    room = Room.objects.get(slug=slug)

    hotel = request.user
    if room.hotel != hotel:
        return Response({'response': 'You do not have permission to delete that'})

    delete = room.delete()
    data = {}
    if delete:
        data['success'] = 'Delete Successful'
    else:
        data['failure'] = 'Delete Failed'
    return Response(data=data)


@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def room_create_api_view(request):
    hotel = request.user
    room = Room(hotel=hotel)
    serializer = RoomSerializer(room, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def all_rooms_api_view(request):
    room = Room.objects.filter(hotel=request.user.id)
    serializer = RoomSerializer(room, many=True)
    return Response(serializer.data)
