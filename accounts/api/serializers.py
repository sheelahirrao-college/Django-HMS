from rest_framework import serializers
from accounts.models import User, Hotel, Customer


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'contact', 'email', 'role', 'hotel', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

        def save(self):
            user = User(
                name=self.validated_data['name'],
                contact=self.validated_data['contact'],
                email=self.validated_data['email'],
                role=self.validated_data['role'],
                hotel=self.validated_data['hotel'],
                username=self.validated_data['username'],
            )
            password = self.validated_data['password']

            user.set_password(password)
            user.save()
            return user


class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'contact', 'slug']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'contact', 'address', 'hotel', 'slug']

