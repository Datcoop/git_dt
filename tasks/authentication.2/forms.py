# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "name@example.com",
                "class": "form-control",
                'id': "correo"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña",
                "class": "form-control",
                "id": "password"
            }
        ))

class SignUpForm(UserCreationForm):
    
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Usuario",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    organizacion = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                "type": "hidden",
                "id": "org",
                "name": "org",
            }
        ))
    tip_user = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                "type": "hidden",
                "id": "tipuser",
                "name": "tipuser",
            }
        ))
#password, last_login, username, email, organizacion, tip_user
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña",
                "class": "form-control",
                "id": "password1"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repetir Contraseña",
                "class": "form-control",
                "id": "password2"
            }
        ))
    nomorg = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Organización",
                "class": "form-control",
                "id": "namorg",
                "style": "width: 200px",
            }
        ))
    pag = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "hidden",
                "id": "nampag",
                "name": "nampag",
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'organizacion', 'tip_user', 'password1', 'password2', 'nomorg', 'pag')
        
        
