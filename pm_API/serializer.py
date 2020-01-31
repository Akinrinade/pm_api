# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import conveyor
print('###############################################checking serializers')

class ConveyorSerializer(serializers.Serializer):
    conveyor_name = serializers.CharField(max_length=20)
    read_time = serializers.IntegerField(required=True)
    read_value = serializers.IntegerField(required=True)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        #return conveyor.objects.create(**validated_data)
        print('validate_data ={}'.format(validated_data))
        return validated_data

