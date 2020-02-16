# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from pandas._libs import json

from .models import *

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import ConveyorSerializer
from pyspc import *
import pandas as pd
import threading
import time
import numpy as np
import seaborn as sns

sns.set()
import matplotlib.pyplot as plt

# Create your views here.
print('###############################################checking views')
max_threshold = 0
min_threshold = 0


def index(request):
    return HttpResponse("Hello, world. You're at my first index.")



def is_outlier(new_read, lower, upper):
    if lower <= new_read <= upper:
        return False
    else:
        return True

def get_agent_data(agentname):

    return conveyor_thresholds.get[agentname]

@api_view(['GET', 'POST'])
def conveyor_list(request):
    """
    List all convetors of a particular conveyor.
    """
    if request.method == 'GET':
        # Treat the GET object
        request_object = {}
        # split get object string to list
        param = request.GET['param'].split(',')
        print(param)
        conveyor_name = str(param[0])
        request_object['Conveyor'] = conveyor_name
        request_object['Time'] = int(param[1])
        request_object['Transport_time'] = float(param[2])
        print(request_object)
        new_read = request_object['Transport_time']

        agent = conveyor_thresholds[conveyor_name]
        #agent = dict(get_agent_data(conveyor_name))
        lower = agent['lower']
        upper = agent['upper']
        outlier = is_outlier(new_read, lower, upper)

        if not outlier:
            print('Value is valid')
            agent_dataframe = agent['dataobject']
            df = agent_dataframe.append(request_object, ignore_index=True)

            agent['dataobject'] = df
            print(df.tail())
            #df[-3:]
            df = df[['Transport_time']].dropna()
            print(df.tail())
            a = spc(df) + ewma() + rules()
            print(a)

            upper_threshold = a.summary[0].get('ucl')[-1]
            lower_threshold = a.summary[0].get('lcl')[-1]

            conveyor_thresholds[conveyor_name]['lower'] = lower_threshold
            conveyor_thresholds[conveyor_name]['upper'] = upper_threshold

            df_plot = format_response(a)
            #agent['dataobject']= df
            print (df_plot.tail())
            plot_view(df_plot, conveyor_name)
            print('Status={}'.format(status.HTTP_201_CREATED))
            response = {"Conveyor_name":conveyor_name,"upper":upper_threshold, "lower": lower_threshold}

            return JsonResponse(response, status=status.HTTP_201_CREATED, safe=False)
        else:
            print('\n Read above Threshold')
            conveyor_thresholds[conveyor_name]['outliers'] = new_read

            agent_dataframe = agent['dataobject']
            df= agent_dataframe.append(request_object, ignore_index=True)
            agent['dataobject'] = df
            df = df[['Transport_time']]
            print(df.tail())
            a = spc(df.dropna()) + ewma() + rules()
            #a = spc(agent_dataframe[['Transport_time']]) + ewma() + rules()
            print(a)
            df_plot=format_response(a)
            print(df_plot.tail())
            plot_view(df_plot, conveyor_name)
            response = {"Conveyor_name": conveyor_name, "upper": upper, "lower": lower}
            #response = json.dump(response)
            return JsonResponse(response, status=status.HTTP_201_CREATED)
    else:
        return  Response('Only "GET" request are treated at this moment', status=status.HTTP_400_BAD_REQUEST)
