# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .models import*

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from serializer import ConveyorSerializer
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at my first index.")


@api_view(['GET', 'POST'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes((IsAuthenticated, ))
def conveyor_list(request):
    """
    List all convetors of a particular conveyor.
    """
    if request.method == 'GET':
        conveyor_object = conveyor.objects.all()
        #conveyor_object = [{'conveyor_name':'ConveyorA', 'read_time': 1500002343, 'read_value': 3445}]
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        print 'authentication_content = {}'.format(content)
        serializer = ConveyorSerializer(conveyor_object, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        conveyor_object = ConveyorSerializer(data=request.data)
        print request.data
        if conveyor_object.is_valid():
            conveyor_object.save()
            return Response(conveyor_object.data, status=status.HTTP_201_CREATED)
        return Response(conveyor_object.errors, status=status.HTTP_400_BAD_REQUEST)