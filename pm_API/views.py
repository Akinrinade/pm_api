# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
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
import seaborn as sns;

sns.set()
import matplotlib.pyplot as plt

# Create your views here.
print('###############################################checking views')
max_threshold = 0
min_threshold = 0


def index(request):
    return HttpResponse("Hello, world. You're at my first index.")


def implement_spc_in_thread(df, finished):
    # a = spc(conveyor_name) + ewma()
    # ax = sns.lineplot(data=df, err_style='band', ci='sd')
    # ax.plot()
    # plt.show()
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
        request_object['conveyor_name'] = conveyor_name
        request_object['read_time'] = int(param[1])
        request_object['read_value'] = int(param[2])
        print(request_object)
        new_read = request_object['read_value']

        agent = conveyor_thresholds[conveyor_name]
        #agent = dict(get_agent_data(conveyor_name))
        lower = agent['lower']
        upper = agent['upper']
        outlier = is_outlier(new_read, lower, upper)

        if not outlier:
            print('Value is valid')
            serializer = ConveyorSerializer(request_object)
            serializer.create(request_object)
            if status.HTTP_201_CREATED:
                df = pd.DataFrame(columns=['Conveyor', 'Time', 'Transport_time'])
                df['Conveyor'] = request_object['conveyor_name']
                df['Time'] = request_object['read_time']
                df['Transport_time'] = request_object['read_value']
                agent_dataframe= agent['dataobject']
                agent_dataframe.append(df)
                conv = agent_dataframe[['Transport_time']]
                ema = conv.ewm(com=0.5).mean()
                ema.columns = ['average']
                a = spc(agent_dataframe[['Transport_time']]) + ewma()
                print(a)
                A = a.summary[0].get('ucl')[-1]
                B = a.summary[0].get('lcl')[-1]

                conveyor_thresholds[conveyor_name]['lower'] = B
                conveyor_thresholds[conveyor_name]['upper'] = A
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
                response = {'Conveyor_name':conveyor_name,'upper':A, 'lower':B}
                #response = conveyor_thresholds[conveyor_name]
                response = json.dumps(response)
                return Response(response, status=status.HTTP_201_CREATED)
        else:
            conveyor_thresholds[conveyor_name]['outliers'] = new_read
            #response = conveyor_thresholds[conveyor_name]
            response = {'Conveyor_name': conveyor_name, 'upper': upper, 'lower': lower}
            return Response(response, status=status.HTTP_201_CREATED)
    else:
        return Response('Only "GET" request are treated at this moment', status=status.HTTP_400_BAD_REQUEST)
