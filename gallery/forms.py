from django import forms
from .models import *

class ImageForm(forms.ModelForm):
   class Meta:
      model = Image
      fields = ['image','name']

class UploadFileForm(forms.ModelForm):
   class Meta:
      model = Archivo
      fields = ['archivo','name']
