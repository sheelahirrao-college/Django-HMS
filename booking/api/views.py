from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from datetime import datetime

from .decorators import role_required, validate_booking_manager
from .permissions import IsSuperUser, IsAdmin, IsStaff
from .serializers import (
    BookingSerializer,
    RoomSerializer,
)

from room.models import Room
from booking.models import Booking
from accounts.models import Hotel, Customer


class BookRoom(APIView):

    permission_classes = [IsAuthenticated, IsSuperUser, IsAdmin, IsStaff]

    def check_availability(self, room, sd, ed):

        bookings = Booking.objects.filter(room=room)

        if not bookings:
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

    @role_required(allowed_roles=[2])
    def get(self, request, slug):

        slug = 'availablerooms'

        start_date = request.data['start_date']
        end_date = request.data['end_date']

        sd = datetime.strptime(start_date, '%Y-%m-%d').date()
        ed = datetime.strptime(end_date, '%Y-%m-%d').date()

        rooms = Room.objects.filter(hotel=request.user.hotel)
        available_rooms = []
        for room in rooms:
            response = self.check_availability(room, sd, ed)
            if response is True:
                available_rooms.append(room)

        if not available_rooms:
            return Response({
                'response': 'No Rooms Available For These Dates'
            })
        else:
            serializer = RoomSerializer(available_rooms, many=True)
            return Response(serializer.data)

    @role_required(allowed_roles=[2])
    def post(self, request, slug):

        try:
            room = Room.objects.get(slug=slug)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        request.data._mutable = True
        request.data['hotel'] = request.user.hotel.id
        request.data['room'] = room.number

        start_date = request.data['start_date']
        end_date = request.data['end_date']

        sd = datetime.strptime(start_date, '%Y-%m-%d').date()
        ed = datetime.strptime(end_date, '%Y-%m-%d').date()

        request.data['no_of_days'] = (ed - sd).days
        request.data._mutable = False

        if sd > ed:
            return Response({
                'response': 'Start Date Must Come Before End Date',
            })

        serializer = BookingSerializer(data=request.data)

        customers = Customer.objects.filter(hotel=request.user.hotel).values('id')
        for c in customers:
            if request.data['customer'] != c['id']:
                pass
            else:
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'response': 'Room Booked Successfully',
                        'data': serializer.data,
                    })
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'response': 'Customer Does Not Exist',
            'customer': c['id'],
        })


class BookedRoomStatus(APIView):

    permission_classes = [IsAuthenticated, IsSuperUser, IsAdmin, IsStaff]

    @role_required(allowed_roles=[2])
    def put(self, request, slug):

        try:
            room = Room.objects.get(slug=slug)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        start_date = request.data['start_date']
        end_date = request.data['end_date']

        sd = datetime.strptime(start_date, '%Y-%m-%d').date()
        ed = datetime.strptime(end_date, '%Y-%m-%d').date()

        if room.booked_from is None and room.booked_to is None:
            request.data._mutable = True
            request.data['booked_from'] = sd
            request.data['booked_to'] = ed
            request.data._mutable = False
        elif room.booked_from <= sd and room.booked_to >= ed:
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
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CustomerBookings(APIView):

    permission_classes = [IsAuthenticated, IsSuperUser, IsAdmin, IsStaff]

    @role_required(allowed_roles=[2])
    def get(self, request, slug):

        if slug == 'allbookings':

            customer = request.data['customer']
            bookings = Booking.objects.filter(customer=customer)
            if not bookings:
                return Response('This Customer Has No Bookings')
            else:
                serializer = BookingSerializer(bookings, many=True)
                return Response(serializer.data)
        else:
            try:
                booking = Booking.objects.get(slug=slug)
            except Booking.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = BookingSerializer(booking)
            return Response(serializer.data)

    @role_required(allowed_roles=[2])
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
