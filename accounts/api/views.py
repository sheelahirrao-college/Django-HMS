from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate

from .permissions import IsHotel, IsRoomManager, IsCustomer
from .serializers import (
    UserRegistrationSerializer,
    HotelSerializer,
    RoomManagerSerializer,
    CustomerSerializer,
    HotelRegistrationSerializer,
)

from accounts.models import User, Hotel, RoomManager, Customer


class UserRegistration(APIView):

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "User Successfully Registered"
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


class UserLogin(APIView):

    def post(self, request):
        context = {}

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)

            context['response'] = 'Successfully Logged In'
            context['token'] = token.key

        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid Credentials'

        return Response(context)


class HotelProfile(APIView):

    permission_classes = [IsAuthenticated, IsHotel]

    def get(self, request):

        try:
            hotel = Hotel.objects.get(user=request.user)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = HotelSerializer(hotel)
        return Response(serializer.data)

    def post(self, request):

        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'response': 'Hotel Successfully Added',
                'data': serializer.data,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):

        try:
            hotel = Hotel.objects.get(user=request.user)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = HotelSerializer(hotel, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'Hotel Updated Successfully'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        user = request.user
        delete = user.delete()

        data = {}

        if delete:
            data['success'] = 'Hotel User Deleted Successfully'
        else:
            data['failed'] = 'Hotel User Delete Failed'

        return Response(data=data)


class RoomManagerProfile(APIView):

    permission_classes = [IsAuthenticated, IsRoomManager]

    def get(self, request):

        try:
            room_manager = RoomManager.objects.get(user=request.user)
        except RoomManager.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RoomManagerSerializer(room_manager)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'response': 'Room Manager Successfully Added',
                'data': serializer.data,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):

        try:
            room_manager = RoomManager.objects.get(user=request.user)
        except RoomManager.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RoomManagerSerializer(room_manager, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'Room Manager Updated Successfully'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        user = request.user
        delete = user.delete()

        data = {}

        if delete:
            data['success'] = 'Room Manager User Deleted Successfully'
        else:
            data['failed'] = 'Room Manager User Delete Failed'

        return Response(data=data)


class CustomerProfile(APIView):

    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'response': 'Customer Successfully Added',
                'data': serializer.data,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):

        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'Customer Updated Successfully'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        user = request.user
        delete = user.delete()

        data = {}

        if delete:
            data['success'] = 'Customer User Deleted Successfully'
        else:
            data['failed'] = 'Customer User Delete Failed'

        return Response(data=data)


class HotelRegistration(APIView):

    def post(self, request):
        serializer = HotelRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Hotel Successfully Registered"
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)
