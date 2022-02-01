from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from room.models import Room
from .serializers import (
    BookingSerializer,
    AvailableRoomSerializer,
)


class Booking(APIView):

    permission_classes = [IsAuthenticated]

    def check_availability(self, request, sd, ed):
        room = Room.objects.all(hotel=request.user.id)
        availablerooms = []
        for r in room:
            bookings = Booking.objects.filter(room=r.number)
            if r.start is None and r.end is None:
                availablerooms.append(True)
            else:
                for booking in bookings:
                    if booking.start_date > ed.date() or booking.end_date < sd.date():
                        availablerooms.append(True)
                    else:
                        availablerooms.append(False)
        return availablerooms

    def post(self, request, slug):

        sd = request.data['start_date']
        ed = request.data['end_date']
        room = Room.objects.filter(slug=slug)
        roomstatus = self.check_availability(sd, ed)

        request.data._mutable = True
        request.data['hotel'] = request.user.id
        request.data['room'] = room.number
        request.data['no_of_days'] = request.data['end_date'] - request.data['start_date']
        request.data._mutable = False

        if request.data['start_date'] >= request.data['end_date']:
            return Response('Start Date must come before End Date')
        else:
            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'response': 'Room Booked Successfully',
                    'data': serializer.data
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomBooking(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        try:
            room = Room.objects.filter(available=True, hotel=request.user.id)
        except Room.DoesNotExist:
            return Response('No Rooms Available')

        slug = 'availablerooms'
        serializer = AvailableRoomSerializer(room, many=True)
        return Response(serializer.data)

    def post(self, request, slug):
        room = Room.objects.get(slug=slug)

        request.data._mutable = True
        request.data['hotel'] = request.user.id
        request.data['room'] = room.number
        request.data._mutable = False
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'response': 'Room Booked Successfully',
                'data': serializer.data
            })
            room.available = True
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)