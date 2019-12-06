# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .spc_spc import preprocessing
# Create your models here.


class conveyor(models.Model):
    conveyor_name = models.CharField(max_length=20)
    read_time = models.IntegerField()
    read_value = models.IntegerField()

    class Meta:
        ordering =['read_time']



filepath = '/home/pi/PycharmProjects/untitled/pm_API/timestamps.csv'
columns= ['Conveyor', 'Action', 'Time']

conveyorA = preprocessing('ConveyorA', columns, filepath)
print(conveyorA.head())
conveyorB = preprocessing('ConveyorB', columns, filepath)
print(conveyorB.head())
conveyorC = preprocessing('ConveyorC', columns, filepath)
print(conveyorC.head())
conveyorD = preprocessing('ConveyorD', columns, filepath)
print(conveyorD.head())
conveyorE = preprocessing('ConveyorE', columns, filepath)
print(conveyorE.head())
conveyorF = preprocessing('ConveyorF', columns, filepath)
print(conveyorF.head())

conveyorA_parameters = {'upper': 2200, 'lower': 1700}
