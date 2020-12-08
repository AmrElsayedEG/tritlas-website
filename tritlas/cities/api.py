from rest_framework import generics
from .models import place,city
from .serializers import PlaceSerializer,CitySerializer
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class PlaceDetail(generics.ListAPIView):
    queryset = place.objects.all()
    serializer_class = PlaceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class OnePlaceDetail(generics.RetrieveAPIView):
    queryset = place.objects.all()
    serializer_class = PlaceSerializer
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class CityDetail(generics.ListAPIView):
    queryset = city.objects.all()
    serializer_class = CitySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class OneCityDetail(generics.RetrieveAPIView):
    queryset = city.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]