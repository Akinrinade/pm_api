# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class conveyor(models.Model):
    conveyor_name = models.CharField(max_length=20)
    read_time = models.IntegerField()
    read_value = models.IntegerField()

    class Meta:
        ordering =['read_time']
