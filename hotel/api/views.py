from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from .serializers import HotelRegistrationSerializer


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


class HotelLoginAPIView(APIView):

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






