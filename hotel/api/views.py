from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import HotelRegistrationSerializer
from rest_framework.authtoken.models import Token

@api_view(['POST',])
def hotel_registration_api_view(request):

    serializer = HotelRegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        hotel = serializer.save()
        data['response'] = "Hotel Successfully Registered"
        data['name'] = hotel.name
        token = Token.objects.get(user=hotel).key
        data['token'] = token
    else:
        data = serializer.errors
    return Response(data)

