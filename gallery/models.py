from django.db import models
from django.contrib.auth.models import User
    
class Image(models.Model):
    image = models.ImageField(upload_to = 'img_coop/')
    name = models.CharField(max_length=200,null=True)
    fecha = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

class Archivo(models.Model):
    archivo = models.FileField(upload_to = "movicoop/")
    name = models.CharField(max_length=200,null=True)
    fecha = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


