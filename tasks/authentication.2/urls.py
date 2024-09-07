# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us 
"""

from django.urls import path
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView

app_name = 'auth'

urlpatterns = [
    path('login/<str:tipuser>', login_view, name="login"),
    path('register/<str:tipuserreg>', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout")
]
