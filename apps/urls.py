# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from apps import views

urlpatterns = [

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
