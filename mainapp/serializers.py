from rest_framework import serializers
from . models import *


class PlacesSerializers(serializers.ModelSerializer):
    class Meta:
        model = TourMorePlaces
        fields = ('id', 'tourplace', 'place_name', 'description', 'category')