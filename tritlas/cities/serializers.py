from rest_framework import serializers
from .models import place,city

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = place
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = city
        fields = '__all__'