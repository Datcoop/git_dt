from django import forms
from .models import Fichas

class ImagesForm(forms.ModelForm):
    class Meta:
        model = Fichas
        fields = ['pic']
