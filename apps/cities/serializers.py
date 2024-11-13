from rest_framework import serializers
from . import models


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.City
        fields = (
            'id', 'name', 'description', 'slug'
        )
        read_only_fields = ('id', 'slug')