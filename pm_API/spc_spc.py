
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


def preprocessing(raw_dataframe, conveyor_name, column_list):

    # load Archived data stored in file as CSV
    #raw_data = pd.read_csv(str(filepath), sep=';', header=None, names=column_list)

    #   get the number unique agent data present in data
    # agents = list(raw_data['Conveyor'].unique())
    # #get the number of Agents


    #filter by conveyor name
    conveyors = raw_dataframe[raw_dataframe['Conveyor'] == conveyor_name]
    conveyor = conveyors[conveyors['Action'] == 'Received']
    conveyor_sent = conveyors[conveyors['Action'] == 'Sent']
    conveyor['Number'] = [i for i in range(1, conveyor.shape[0]+1)]
    conveyor.set_index(keys =['Number'])
    conveyor_sent['Number'] = [i for i in range(1, conveyor_sent.shape[0]+1)]
    conveyor_sent.set_index(keys =['Number'])
    conveyor_sent.columns =['Conveyor2', 'Action2', 'Time2', 'Number']

    conveyor = pd.merge(conveyor, conveyor_sent, on='Number')
    conveyor['Transport_time'] = conveyor['Time2'] - conveyor['Time']
    print(conveyor['Transport_time'].max())
    print(conveyor['Transport_time'].min())
    conveyor_processed = conveyor[['Conveyor', 'Time', 'Transport_time']]
    return conveyor_processed
