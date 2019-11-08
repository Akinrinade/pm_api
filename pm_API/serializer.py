# -*- coding: utf-8 -*-

from rest_framework import serializers
from models import conveyor

class ConveyorSerializer(serializers.Serializer):
    conveyor_name = serializers.CharField(max_length=20)
    read_time = serializers.IntegerField()
    read_value = serializers.IntegerField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return conveyor.objects.create(**validated_data)

