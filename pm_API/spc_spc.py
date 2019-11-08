
import pandas as pd
import numpy as np
#import seaborn as sb

# a = spc(pistonrings) + ewma()
# print(a)
#
# a+ rules()
pd.set_option("display.max_rows", 100)
pd.set_option("display.max_columns", 100)


def preprocessing(conveyor_name, column_list, filepath):

    # columns= ['Conveyor', 'Action', 'Time']
    raw_data = pd.read_csv(filepath, sep=';', header=None, names=column_list)
    #print(raw_data.head())

    conveyors = raw_data[raw_data['Conveyor'] == conveyor_name]
    #print (conveyors.head())
    conveyor = conveyors[conveyors['Action'] == 'Received']
    conveyor_sent = conveyors[conveyors['Action'] == 'Sent']

    conveyor['Number'] = [i for i in range(1, conveyor.shape[0]+1)]
    conveyor.set_index(keys =['Number'])
    conveyor_sent['Number'] = [i for i in range(1, conveyor_sent.shape[0]+1)]
    conveyor_sent.set_index(keys =['Number'])
    conveyor_sent.columns =['Conveyor2', 'Action2', 'Time2', 'Number']
    # print (conveyor_sent.head())
    conveyor = pd.merge(conveyor, conveyor_sent, on='Number')
    # conveyor_A['Sent_time'] = ConveyorA_sent['Time']
    # conveyor_A['Transport_time'] = conveyor_A['Sent_time'] - conveyor_A['Time']
    #print (conveyor.head())
    #print (conveyors.head())
    conveyor['Transport_time'] = conveyor['Time2'] - conveyor['Time']
    print(conveyor.head())
    print(conveyor.tail())
    print(conveyor['Transport_time'].max())
    print(conveyor['Transport_time'].min())
    conveyor_processed = conveyor[['Number', 'Transport_time']]
    return conveyor_processed
