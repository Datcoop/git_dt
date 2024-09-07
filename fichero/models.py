from django.db import models
from django.contrib.auth.models import User

class Fichas(models.Model):
    pic = models.FileField(upload_to='carpArch')  
    uploaded_at = models.DateTimeField(auto_now_add=True)      
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE) 
