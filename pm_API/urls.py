# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from django.urls import path


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'conveyor_list', views.conveyor_list, name='conveyor_list'),
    path(r'conveyor_list/<str:param>', views.conveyor_list, name='conveyor_list'),
    url(r'^api-auth/', include('rest_framework.urls')),
]
