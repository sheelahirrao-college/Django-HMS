from rest_framework import serializers
from accounts.models import User, Hotel, RoomManager, Customer


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'usertype']
        extra_kwargs = {
            'password': {'write_only': True},
        }

        def save(self):
            user = User(
                email=self.validated_data['email'],
                username=self.validated_data['username'],
            )
            password = self.validated_data['password']

            user.set_password(password)
            user.save()
            return user


class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = ['user', 'name', 'contact']


class RoomManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomManager
        fields = ['user', 'name', 'contact', 'hotel']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user', 'name', 'contact']


class HotelDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = ['name', 'contact']


class HotelRegistrationSerializer(serializers.ModelSerializer):

    hotel = HotelDataSerializer()

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'usertype', 'hotel']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            usertype=validated_data['usertype'],
        )

        hotel_data = validated_data.pop('hotel')
        hotel = Hotel.objects.create(
            user=user,
            name=hotel_data['name'],
            contact=hotel_data['contact'],
        )
        return user