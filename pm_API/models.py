# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from pyspc import spc, ewma

from .spc_spc import preprocessing, load_archived_data, uniques_agents

# Create your models here.

# conveyor_thresholds = {
#     'ConveyorA': {'upper': 2200, 'lower': 1700, 'outliers': []},
#     'ConveyorB': {'upper': 2200, 'lower': 1700, 'outliers': []},
#     'ConveyorC': {'upper': 2200, 'lower': 1700, 'outliers': []},
#     'ConveyorD': {'upper': 2200, 'lower': 1700, 'outliers': []},
#     'ConveyorE': {'upper': 2200, 'lower': 1700, 'outliers': []},
#     'ConveyorF': {'upper': 2200, 'lower': 1700, 'outliers': []},
# }

print('###############################################checking models')
class conveyor(models.Model):
    conveyor_name = models.CharField(max_length=20)
    read_time = models.IntegerField()
    read_value = models.IntegerField()

    class Meta:
        ordering =['read_time']






filepath = '/home/pi/PycharmProjects/untitled/pm_API/timestamps.csv'
columns = ['Conveyor', 'Action', 'Time']

conveyor_thresholds={}
raw_dataframe = load_archived_data(filepath, columns)

agents, no_agents = uniques_agents(raw_dataframe)

agents_data=[]
print('Agents found in data = {}'.format(str(agents)))

for agent in agents:
    agentdata = preprocessing(raw_dataframe, agent, columns)
    # = preprocessing(raw_dataframe, agent, columns)
    agent_data = {'name': agent, 'upper': 2200, 'lower': 1700, 'outliers': []}
    print(agentdata.head())
    a = spc(agentdata[['Transport_time']]) + ewma()
    print(a)
    A = a.summary[0].get('ucl')[-1]
    B = a.summary[0].get('lcl')[-1]
    agent_data['lower'] = B
    agent_data['upper'] = A
    agent_data['dataobject']=agentdata
    conveyor_thresholds[agent]=agent_data
    # conveyor_thresholds[agent]['lower'] = B
    # conveyor_thresholds[agent]['upper'] = A

# conveyorA = preprocessing(raw_dataframe, 'ConveyorA', columns)
# print(conveyorA.head())
# a = spc(conveyorA[['Transport_time']]) + ewma()
# print(a)
# A = a.summary[0].get('ucl')[-1]
# B = a.summary[0].get('lcl')[-1]
# conveyor_thresholds['ConveyorA']['lower'] = B
# conveyor_thresholds['ConveyorA']['upper'] = A
#
#
# conveyorB = preprocessing(raw_dataframe, 'ConveyorB', columns)
# print(conveyorB.head())
# a = spc(conveyorB[['Transport_time']]) + ewma()
# print(a)
# A = a.summary[0].get('ucl')[-1]
# B = a.summary[0].get('lcl')[-1]
# conveyor_thresholds['ConveyorB']['lower'] = B
# conveyor_thresholds['ConveyorB']['upper'] = A
#
# conveyorC = preprocessing(raw_dataframe, 'ConveyorC', columns)
# print(conveyorC.head())
# a = spc(conveyorC[['Transport_time']]) + ewma()
# print(a)
# A = a.summary[0].get('ucl')[-1]
# B = a.summary[0].get('lcl')[-1]
# conveyor_thresholds['ConveyorC']['lower'] = B
# conveyor_thresholds['ConveyorC']['upper'] = A
#
# conveyorD = preprocessing(raw_dataframe, 'ConveyorD', columns)
# print(conveyorD.head())
# a = spc(conveyorD[['Transport_time']]) + ewma()
# print(a)
# A = a.summary[0].get('ucl')[-1]
# B = a.summary[0].get('lcl')[-1]
# conveyor_thresholds['ConveyorD']['lower'] = B
# conveyor_thresholds['ConveyorD']['upper'] = A
#
# conveyorE = preprocessing(raw_dataframe, 'ConveyorE', columns)
# print(conveyorE.head())
# a = spc(conveyorE[['Transport_time']]) + ewma()
# print(a)
# A = a.summary[0].get('ucl')[-1]
# B = a.summary[0].get('lcl')[-1]
# conveyor_thresholds['ConveyorE']['lower'] = B
# conveyor_thresholds['ConveyorE']['upper'] = A
#
# conveyorF = preprocessing(raw_dataframe, 'ConveyorF', columns)
# print(conveyorF.head())
# a = spc(conveyorF[['Transport_time']]) + ewma()
# print(a)
# A = a.summary[0].get('ucl')[-1]
# B = a.summary[0].get('lcl')[-1]
# conveyor_thresholds['ConveyorF']['lower'] = B
# conveyor_thresholds['ConveyorF']['upper'] = A




