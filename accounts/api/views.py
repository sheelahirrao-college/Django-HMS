from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import HotelRegistrationSerializer, RoomManagerRegistrationSerializer, CustomerRegistrationSerializer


class HotelRegistrationAPIView(APIView):

    def post(self, request):
        serializer = HotelRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            hotel = serializer.save()
            data['response'] = "Hotel Successfully Registered"
            token = Token.objects.get(user=hotel).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


class HotelLoginView(APIView):

    def post(self, request):
        context = {}

        username = request.POST.get('username')
        password = request.POST.get('password')

        hotel = authenticate(username=username, password=password)

        if hotel:
            try:
                token = Token.objects.get(user=hotel)
            except Token.DoesNotExist:
                token = Token.objects.create(user=hotel)

            context['response'] = 'Successfully Logged In'
            context['token'] = token.key

        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid Credentials'

        return Response(context)


class RoomManagerRegistrationAPIView(APIView):

    def post(self, request):
        serializer = RoomManagerRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            hotel = serializer.save()
            data['response'] = "Room Manager Successfully Registered"
            token = Token.objects.get(user=hotel).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


class RoomManagerLoginView(APIView):

    def post(self, request):
        context = {}

        username = request.POST.get('username')
        password = request.POST.get('password')

        hotel = authenticate(username=username, password=password)

        if hotel:
            try:
                token = Token.objects.get(user=hotel)
            except Token.DoesNotExist:
                token = Token.objects.create(user=hotel)

            context['response'] = 'Room Manager Successfully Logged In'
            context['token'] = token.key

        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid Credentials'

        return Response(context)


class CustomerRegistrationAPIView(APIView):

    def post(self, request):
        serializer = CustomerRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            hotel = serializer.save()
            data['response'] = "Customer Successfully Registered"
            token = Token.objects.get(user=hotel).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


class CustomerLoginView(APIView):

    def post(self, request):
        context = {}

        username = request.POST.get('username')
        password = request.POST.get('password')

        customer = authenticate(username=username, password=password)

        if customer:
            try:
                token = Token.objects.get(user=customer)
            except Token.DoesNotExist:
                token = Token.objects.create(user=customer)

            context['response'] = 'Successfully Logged In'
            context['token'] = token.key

        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid Credentials'

        return Response(context)