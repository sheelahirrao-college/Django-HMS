from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from datetime import datetime

from room.models import Room
from booking.models import Booking
from accounts.models import Hotel

from .serializers import (
    BookingSerializer,
    RoomSerializer,
    RoomDetailsSerializer,
)


class AvailableRooms(APIView):

    permission_classes = [IsAuthenticated]

    def check_availability(self, room, sd, ed):

        bookings = Booking.objects.filter(room=room)

        if not(bookings):
            return True
        else:
            if room.booked_from is None and room.booked_to is None:
                for booking in bookings:
                    if booking.start_date > ed or booking.end_date < sd:
                        return True
                    else:
                        return False
            else:
                if room.booked_from > ed or room.booked_to < sd:
                    for booking in bookings:
                        if booking.start_date > ed or booking.end_date < sd:
                            return True
                        else:
                            return False

    def get(self, request):

        start_date = request.data['start_date']
        end_date = request.data['end_date']

        sd = datetime.strptime(start_date, '%Y-%m-%d').date()
        ed = datetime.strptime(end_date, '%Y-%m-%d').date()

        rooms = Room.objects.all()
        available_rooms = []
        for room in rooms:
            response = self.check_availability(room, sd, ed)
            if response is True:
                available_rooms.append(room)

        serializer = RoomDetailsSerializer(available_rooms, many=True)
        return Response(serializer.data)


class BookRoom(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        try:
            room = Room.objects.get(slug=slug)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RoomDetailsSerializer(room)
        return Response(serializer.data)

    def post(self, request, slug):

        try:
            room = Room.objects.get(slug=slug)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            hotel = Hotel.objects.get(user=request.user)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        request.data._mutable = True
        request.data['hotel'] = hotel.id
        request.data['room'] = room.number

        start_date = request.data['start_date']
        end_date = request.data['end_date']

        sd = datetime.strptime(start_date, '%Y-%m-%d').date()
        ed = datetime.strptime(end_date, '%Y-%m-%d').date()

        request.data['no_of_days'] = (ed - sd).days
        request.data._mutable = False

        if sd > ed:
            return Response('Start Date must come before End Date')
        else:
            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'response': 'Room Booked Successfully',
                    'data': serializer.data,
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):

        try:
            booking = Booking.objects.get(slug=slug)
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        delete = booking.delete()
        data = {}
        if delete:
            data['success'] = 'Booking Cancelled Successfully'
        else:
            data['failure'] = 'Booking Cancellation Failed'
        return Response(data=data)


class RoomBookedStatus(APIView):

    def put(self, request, slug):

        try:
            room = Room.objects.get(slug=slug)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        start_date = request.data['start_date']
        end_date = request.data['end_date']

        sd = datetime.strptime(start_date, '%Y-%m-%d').date()
        ed = datetime.strptime(end_date, '%Y-%m-%d').date()

        if room.booked_from <= sd and room.booked_to >= ed:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data._mutable = True
            request.data['booked_from'] = sd
            request.data['booked_to'] = ed
            request.data._mutable = False

        serializer = RoomSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Room Booked Status Updated Successfully')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Bookings(APIView):

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)