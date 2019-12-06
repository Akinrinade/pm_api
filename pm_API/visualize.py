
from pyspc import *
import numpy as np
#from spc_spc import *
import seaborn as sb
from .spc_spc import *

from untitled.pm_API.spc_spc import preprocessing

filepath ='timestamps.csv'
columns= ['Conveyor', 'Action', 'Time']

conveyorA = preprocessing('ConveyorA', columns, filepath)
conveyorB = preprocessing('ConveyorB', columns, filepath)
conveyorC = preprocessing('ConveyorC', columns, filepath)
conveyorD = preprocessing('ConveyorD', columns, filepath)
conveyorE = preprocessing('ConveyorE', columns, filepath)
conveyorF = preprocessing('ConveyorF', columns, filepath)

a = spc(pistonrings) + ewma()
print(a)
#a = spc(conveyorA) + ewma()
#print(a)

#b = spc(conveyorB) + ewma()
#print(b)
#c = spc(conveyorC) + ewma()
#rint(c)
#d = spc(conveyorD) + ewma()
#print(d)
#e = spc(conveyorE) + ewma()
#print(e)
#f = spc(conveyorF) + ewma()
#print(f)

print (conveyorA.head())
#print conveyorB.head()
#print conveyorC.head()
#print conveyorD.head()
#print conveyorE.head()
#print conveyorF.head()
