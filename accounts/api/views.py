from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import (
    UserRegistrationSerializer,
    HotelSerializer,
    RoomManagerSerializer,
    CustomerSerializer,
    HotelRegistrationSerializer,
)


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


class Hotel(APIView):

    def post(self, request):
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'response': 'Hotel Successfully Added',
                'data': serializer.data,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomManager(APIView):

    def post(self, request):
        serializer = RoomManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'response': 'Room Manager Successfully Added',
                'data': serializer.data,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Customer(APIView):

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'response': 'Customer Successfully Added',
                'data': serializer.data,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
