
import pandas as pd
import numpy as np

pd.set_option("display.max_rows", 100)
pd.set_option("display.max_columns", 100)



def uniques_agents(raw_dataframe):
    # get the number unique agent data present in data
    agents = list(raw_dataframe['Conveyor'].unique())
    # get the number of Agents
    no_of_agents = len(agents)
    return agents, no_of_agents



def load_archived_data(filepath, column_list):
    raw_dataframe = pd.read_csv(str(filepath), sep=';', header=None, names=column_list)
    return raw_dataframe


def get_action_dfs(raw_dataframe, action1, action2):
    actions_df1 = raw_dataframe[raw_dataframe['Action'] == action1]
    actions_df2 = raw_dataframe[raw_dataframe['Action'] == action2]
    return actions_df1, actions_df2


def calculate(raw_dataframe):
    raw_dataframe['Next Conveyor']=raw_dataframe['Conveyor'].shift(-1)
    raw_dataframe['Received Time'] = raw_dataframe['Time'].shift(-1)
    raw_dataframe['Transport_time']= raw_dataframe['Received Time'] - raw_dataframe['Time']
    print ('Raw dataframe head after calculate ={}'.format(raw_dataframe.head()))
    sent_df = raw_dataframe[raw_dataframe['Action']=='Sent']
    print('Filtered sent df  = {}'.format(sent_df.head()))
    sent_df= sent_df[['Conveyor', 'Time', 'Transport_time']]
    return sent_df


