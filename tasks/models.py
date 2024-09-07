from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=1000)
  created = models.DateTimeField(auto_now_add=True)
  datecompleted = models.DateTimeField(null=True, blank=True)
  important = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title + ' - ' + self.user.username

class Contacto(models.Model):
  rif = models.CharField(max_length=20)
  nomorg = models.CharField(max_length=100)
  correo = models.CharField(max_length=100)
  mensaje = models.TextField(max_length=1000)
  asunto = models.CharField(max_length=200, default='Asunto')
  created = models.DateTimeField(auto_now_add=True)
  telefono = models.CharField(max_length=50,null=False)

  def __str__(self):
    return self.nomorg
        
class Sociosjson(models.Model): 
    codigo = models.JSONField(null=True, blank=True)          
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)        
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
class Fichero(models.Model):
    titulo = models.CharField(max_length=255, blank=True)
    pic = models.FileField(upload_to='Archivos') 
    uploaded_at = models.DateTimeField(auto_now_add=True)          
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE) 
        
class Movimientos(models.Model): 
    archivo = models.JSONField(null=True, blank=True)         
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
class Movsocios(models.Model):
    fecha = models.DateTimeField(auto_now_add=True) 
    referencia = models.CharField(max_length=25, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
class Movisocios(models.Model):
    fecha = models.DateTimeField(auto_now_add=True) 
    referencia = models.CharField(max_length=25, blank=True)
    socio = models.CharField(max_length=25, null=True, blank=True)
    fechachk = models.DateTimeField(null=True, blank=True)
    
class Movbancos(models.Model):
    fecha = models.DateTimeField(null=True, blank=True) 
    referencia = models.CharField(max_length=25, blank=True)
    codigo = models.CharField(max_length=3, blank=True)
    descripcion = models.CharField(max_length=100, blank=True)                       
    debito = models.FloatField(blank=True, null=True)                       
    credito = models.FloatField(blank=True, null=True)                       
    saldo = models.FloatField(blank=True, null=True) 
    
class Movcoop(models.Model):
    fecha = models.DateTimeField(null=True, blank=True) 
    referencia = models.CharField(max_length=25, blank=True)
    codigo = models.CharField(max_length=3, blank=True)
    descripcion = models.CharField(max_length=100, blank=True)                       
    debito = models.FloatField(blank=True, null=True)                       
    credito = models.FloatField(blank=True, null=True)                       
    saldo = models.FloatField(blank=True, null=True) 
    
class Permisostbl(models.Model):
    tipuser = models.IntegerField(null=True, blank=True) 
    tablas = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
class Cooperativas(models.Model):
    rif = models.CharField(max_length=20, blank=True)
    nombre = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    estatus = models.CharField(max_length=10, blank=True) 
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    
class Socios(models.Model):
    codigo = models.IntegerField(null=True, blank=True, unique=True)
    nombre = models.CharField(max_length=100, blank=True)
    sexo = models.CharField(max_length=15, blank=True)
    estatus = models.CharField(max_length=10, blank=True) 
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    coop = models.IntegerField(null=True, blank=True) 
    
class Tasas(models.Model):
    tasa = models.FloatField(null=True, blank=True)
    fecha = models.DateTimeField(null=True, blank=True)
    
class Bancos(models.Model):
    codigo = models.CharField(max_length=6, blank=True)
    nombre = models.CharField(max_length=100, blank=True)

class Sexo(models.Model):
    sexo = models.CharField(max_length=10, null=True, blank=True)

class Estatus(models.Model):
    estatus = models.CharField(max_length=12, null=True, blank=True)
    
    

    
    
    
    
    
    
    
    
    
    
    
