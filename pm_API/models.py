# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from pyspc import spc, ewma, rules

from .spc_spc import load_archived_data, uniques_agents, get_action_dfs, calculate
import seaborn as sns

sns.set()
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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



def plot_view(df, agent):
    ax = sns.lineplot(data=df, hue=df.columns)
    ax.plot()
    ax.set_title(agent)
    ax.set_xticks(ax.get_xticks()[::20])
    plt.show()
    plt.savefig()


def format_response(response):
    df = pd.DataFrame()
    df['values'] = [list(i)[0]for i in response.summary[0].get('values')]
    df['upper_threshold'] = list(response.summary[0].get('ucl'))
    df['lower_threshold'] = list(response.summary[0].get('lcl'))

    df.dropna()
    df['count'] = list(range(1, len(df['values']) + 1))
    df.set_index('count', inplace=True)
    return df

filepath = '/home/pi/PycharmProjects/untitled/pm_API/timestamps.csv'
columns = ['Conveyor', 'Action', 'Time']

conveyor_thresholds={}
raw_dataframe = load_archived_data(filepath, columns)

agents, no_agents = uniques_agents(raw_dataframe)

agents_data=[]
print('Agents found in data = {}'.format(str(agents)))

#agent_dict = calculate(raw_dataframe, sent_df, receive_df)
processed_raw  = calculate(raw_dataframe.copy())
#print (agent_dict)
#agents = ['ConveyorB']

for agent in agents:

    agentdata= processed_raw[processed_raw['Conveyor']==str(agent)]

    agent_data = {'name': agent, 'upper': 2200, 'lower': 1700, 'outliers': []}

    #print(agentdata[['Transport_time']].dropna())
    a = spc(agentdata[['Transport_time']].dropna(), title=str(agent)+"_ewma") + ewma() + rules()
    print(a)
    #print(a.summary)
    upper_threshold = a.summary[0].get('ucl')[-1]
    lower_threshold = a.summary[0].get('lcl')[-1]
    #print(a.summary[0])
    df = format_response(a)
    print(df.head())
    plot_view(df, str(agent))
    print('{} lower thresold ={}'.format(agent, lower_threshold))
    print('{} upper thresold ={}'.format(agent, upper_threshold))

    agent_data['lower'] = lower_threshold
    agent_data['upper'] = upper_threshold
    agent_data['dataobject'] = agentdata
    agent_data['cleandata'] = agentdata
    conveyor_thresholds[agent] = agent_data




