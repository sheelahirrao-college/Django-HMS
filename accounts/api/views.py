from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate

from .permissions import IsSuperUser, IsAdmin, IsStaff
from .serializers import (
    UserRegistrationSerializer,
    HotelSerializer,
    CustomerSerializer,
)

from accounts.models import User, Hotel, Customer


class UserRegistration(APIView):

    def post(self, request):

        serializer = UserRegistrationSerializer(data=request.data)
        data = {}

        try:
            hotel = Hotel.objects.get(id=request.data['hotel'])
        except Hotel.DoesNotExist:
            return Response('Hotel Does Not Exist')

        if hotel:
            if serializer.is_valid():
                user = serializer.save()
                data['response'] = "User Successfully Registered"
                token = Token.objects.get(user=user).key
                data['token'] = token
            else:
                data = serializer.errors
            return Response(data)
        else:
            return Response('Hotel Does Not Exist')


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

    permission_classes = [IsAuthenticated, IsSuperUser, IsAdmin, IsStaff]

    def get(self, request, slug):

        try:
            hotel = Hotel.objects.get(slug=slug)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.hotel != hotel or request.user.is_superuser is False:
            return Response({
                'response': 'You Cannot View The Hotel Details - Only Users Related To Hotel Can',
            })
        else:
            serializer = HotelSerializer(hotel)
            return Response(serializer.data)

    def post(self, request, slug):

        slug = 'newhotel'

        if request.user.is_superuser is False:
            return Response({
                'response': 'You Cannot Add A Hotel - Only Superusers Can',
            })
        else:
            serializer = HotelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'response': 'Hotel Successfully Added',
                    'data': serializer.data,
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, slug):

        try:
            hotel = Hotel.objects.get(slug=slug)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.hotel != hotel or request.user.is_superuser is False:
            return Response({
                'response': 'You Cannot Edit The Hotel Details - Only Users Related To Hotel Can',
            })
        else:
            serializer = HotelSerializer(hotel, data=request.data, partial=True)
            data = {}
            if serializer.is_valid():
                serializer.save()
                data['response'] = 'Hotel Updated Successfully'
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):

        try:
            hotel = Hotel.objects.get(slug=slug)
        except Hotel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.hotel != hotel or request.user.is_superuser is False:
            return Response({
                'response': 'You Cannot Delete The Hotel - Only Users Related To Hotel Can',
            })
        else:
            delete = hotel.delete()
            data = {}
            if delete:
                data['success'] = 'Hotel Deleted Successfully'
            else:
                data['failed'] = 'Hotel Delete Failed'

            return Response(data=data)


class CustomerProfile(APIView):

    permission_classes = [IsAuthenticated, IsSuperUser, IsAdmin, IsStaff]

    def get(self, request, slug):

        if request.user.role != 3 or request.user.is_superuser is False:
            return Response({
                'response': 'You Cannot View The Customer Details - Only Customer Managers Can',
            })
        else:
            try:
                customer = Customer.objects.get(slug=slug)
            except Customer.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = CustomerSerializer(customer)
            return Response(serializer.data)

    def post(self, request, slug):

        slug = 'newcustomer'

        if request.user.role != 3 or request.user.is_superuser is False:
            return Response({
                'response': 'You Cannot Add A Customer - Only Customer Managers Can',
            })
        else:
            try:
                hotel = Hotel.objects.get(name=request.user.hotel)
            except Hotel.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            request.data._mutable = True
            request.data['hotel'] = hotel.id
            request.data._mutable = False

            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'response': 'Customer Successfully Added',
                    'data': serializer.data,
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, slug):

        if request.user.role != 3 or request.user.is_superuser is False:
            return Response({
                'response': 'You Cannot Edit The Customer Details - Only Customer Managers Can',
            })
        else:
            try:
                customer = Customer.objects.get(slug=slug)
            except Customer.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = CustomerSerializer(customer, data=request.data, partial=True)
            data = {}
            if serializer.is_valid():
                serializer.save()
                data['response'] = 'Customer Updated Successfully'
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):

        if request.user.role != 3 or request.user.is_superuser is False:
            return Response({
                'response': 'You Cannot Delete The Customer - Only Customer Managers Can',
            })
        else:
            try:
                customer = Customer.objects.get(slug=slug)
            except Customer.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            delete = customer.delete()

            data = {}

            if delete:
                data['success'] = 'Customer Deleted Successfully'
            else:
                data['failed'] = 'Customer Delete Failed'

            return Response(data=data)
