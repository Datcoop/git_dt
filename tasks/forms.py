
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from .models import Task, Contacto
from .models import Photo, Fichero

class FicheroForm(forms.ModelForm):
    class Meta:
        model = Fichero
        fields = ['pic']

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class FileFieldForm(forms.Form):
    file_field = MultipleFileField()        
    
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file', )

class LoginForm(forms.Form):  
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Usuario",
                "class": "form-control",
                'id': "cirif"
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
#id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined    
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Usuario",
                "class": "form-control",
                'id': "cirif"
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

    class Meta:
        model = User
        fields = ('username', 'email', 'organizacion', 'tip_user', 'password1', 'password2')

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']

class ContacForm(ModelForm):
    
    rif = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "RIF",
                "class": "form-control",
                'id': "rif"
            }
        ))
    
    nomorg = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Cooperativa",
                "class": "form-control",
                'id': "nomorg"
            }
        ))  
    telef = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Teléfono",
                "class": "form-control",
                'id': "telefono"
            }
        ))        
    correo = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "name@example.com",
                "class": "form-control",
                'id': "correo"
            }
        ))
        
    asunto = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Asunto",
                "class": "form-control",
                'id': "asunto"
            }
        ))
        
    mensaje = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Mensaje",
                "class": "form-control",
                'id': "mensaje",
                'rows': "5"
            }
        ))

    class Meta:
        model = Contacto
        fields = ('rif', 'nomorg', 'telef', 'correo', 'asunto', 'mensaje')
        
        
        
        
