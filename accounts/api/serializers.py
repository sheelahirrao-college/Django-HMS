from rest_framework import serializers
from accounts.models import Hotel, RoomManager, Customer


class HotelRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['name', 'email', 'contact', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        hotel = Hotel(
            name=self.validated_data['name'],
            email=self.validated_data['email'],
            contact=self.validated_data['contact'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']

        hotel.set_password(password)
        hotel.save()
        return hotel


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'contact', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        customer = Customer(
            name=self.validated_data['name'],
            email=self.validated_data['email'],
            contact=self.validated_data['contact'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']

        customer.set_password(password)
        customer.save()
        return customer


class RoomManagerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomManager
        fields = ['name', 'email', 'contact', 'username', 'password', 'hotel']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        room_manager = RoomManager(
            name=self.validated_data['name'],
            email=self.validated_data['email'],
            contact=self.validated_data['contact'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']

        room_manager.set_password(password)
        room_manager.save()
        return room_manager
