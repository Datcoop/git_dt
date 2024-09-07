# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from tasks import views

app_name = 'aplic'

urlpatterns = [
    path('pages/<int:redirh>/<str:ruta>', views.pages, name='pages'),
    path('administrar/', views.administrar, name='administrar'),
    # Matches any html file
    #re_path(r'^.*\.*', views.pages, name='pages'),

]
