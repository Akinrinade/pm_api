# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from pandas._libs import json

from .models import*

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import ConveyorSerializer
from pyspc import *
import pandas as pd
import threading
import time
import numpy as np
import seaborn as sns;sns.set()
import matplotlib.pyplot as plt
# Create your views here.

max_threshold = 0
min_threshold = 0
def index(request):
    return HttpResponse("Hello, world. You're at my first index.")


def implement_spc_in_thread(df, finished):
    #a = spc(conveyor_name) + ewma()
    #ax = sns.lineplot(data=df, err_style='band', ci='sd')
    #ax.plot()
    #plt.show()
    # print(a)
    # max_threshold = a.summary[0].get('ucl')[-1]
    # min_threshold = a.summary[0].get('lcl')[-1]
    print('min_threahold={}'.format(min_threshold))
    print('thread done!!')
    finished = True
    return finished

def plot_view(min, max):

    ax = sns.lineplot(data=min, err_style='band', ci='sd')
    ax.plot()
    ax = sns.lineplot(data=max, err_style='band', ci='sd')
    ax.plot()
    plt.savefig()


@api_view(['GET', 'POST'])
def conveyor_list(request):
    """
    List all convetors of a particular conveyor.
    """
    if request.method == 'GET':
        conveyor_object = conveyor.objects.all()
        #conveyor_object = [{'conveyor_name':'ConveyorA', 'read_time': 1500002343, 'read_value': 3445}]
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        print('authentication_content = {}'.format(content))
        print(request.GET)
        print(request.GET['param'])
        request_object = {}
        param = request.GET['param'].split(',')
        request_object['conveyor_name'] =param[0]
        request_object['read_time'] = int(param[1])
        request_object['read_value'] = int(param[2])

        f = request_object['read_value']
        if f >= conveyorA_parameters['lower'] and f <= conveyorA_parameters['upper']:
            print('Value is valid')
            serializer = ConveyorSerializer(request_object)
            serializer.create(request_object)
            if status.HTTP_201_CREATED:
                df = pd.DataFrame(columns=['Conveyor', 'Time', 'Transport_time'])
                df['Conveyor'] = request_object['conveyor_name']
                df['Time'] = request_object['read_time']
                df['Transport_time'] = request_object['read_value']
                conveyorA.append(df)
                conv = conveyorA[['Transport_time']]
                finished = False
                ema = conv.ewm(com=0.5).mean()
                ema.columns = ['average']

                a = spc(conveyorA[['Transport_time']]) + ewma()

                print(a)

                A = a.summary[0].get('ucl')[-1]
                B = a.summary[0].get('lcl')[-1]

                print(max_threshold)
                print(min_threshold)

                print('ema.columns={}'.format(ema.columns))
                mean = ema['average'][-1:]

                print('type = {}'.format(type(mean)))
                stds = ema['average'].std()
                print('ema.head={}'.format(ema))
                print('standard deviation={}'.format(stds))
                print('Mean={}'.format(mean))
                print('lower_threshold ={}'.format(mean - stds))
                print('upper_threshold ={}'.format(mean + stds))
                print('Status={}'.format(status.HTTP_201_CREATED))
                response = {'upper':A, 'lower':B}
                #response = json.dumps(response)
                return Response(response, status=status.HTTP_201_CREATED)
        #serializer = ConveyorSerializer(conveyor_object, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print('request={}'.format(request))
        print('request.data={}'.format(request.data))

        for item in request.data:
            print('item= {}'.format(item))
            request_object = json.loads(item)
            print(request_object)
            request_object['read_time'] = int(request_object['read_time'])
            request_object['read_value'] = int(request_object['read_value'])

            f=request_object['read_value']
            if f >= conveyorA_parameters['lower'] and f <= conveyorA_parameters['upper']:
                print('Value is valid')
                serializer = ConveyorSerializer(request_object)
                serializer.create(request_object)
                if status.HTTP_201_CREATED:
                    df=pd.DataFrame(columns=['Conveyor','Time','Transport_time'])
                    df['Conveyor'] = request_object['conveyor_name']
                    df['Time'] = request_object['read_time']
                    df['Transport_time'] = request_object['read_value']
                    conveyorA.append(df)
                    conv = conveyorA[['Transport_time']]
                    finished=False
                    ema = conv.ewm(com=0.5).mean()
                    ema.columns = ['average']

                    a = spc(conveyorA[['Transport_time']]) + ewma()

                    print(a)
                    #print(a.summary[0].get('ucl').mean)
                    A = a.summary[0].get('ucl')[-1]
                    B = a.summary[0].get('lcl')[-1]
                    #plot_
                    print(max_threshold)
                    print(min_threshold)

                    print('ema.columns={}'.format(ema.columns))
                    mean = ema['average'][-1:]

                    print('type = {}'.format(type(mean)))
                    stds = ema['average'].std()
                    print('ema.head={}'.format(ema))
                    print('standard deviation={}'.format(stds))
                    print('Mean={}'.format(mean))
                    print('lower_threshold ={}'.format(mean-stds))
                    print('upper_threshold ={}'.format(mean + stds))
                    print('Status={}'.format(status.HTTP_201_CREATED))
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print('value not within threshold')

            return Response('value not within  Threshold', status=status.HTTP_400_BAD_REQUEST)