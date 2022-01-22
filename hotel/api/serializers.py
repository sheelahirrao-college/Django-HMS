from rest_framework import serializers
from hotel.models import Hotel


class HotelRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['name', 'description', 'email', 'contact', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        hotel = Hotel(
            name=self.validated_data['name'],
            description=self.validated_data['description'],
            email=self.validated_data['email'],
            contact=self.validated_data['contact'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']

        hotel.set_password(password)
        hotel.save()
        return hotel
