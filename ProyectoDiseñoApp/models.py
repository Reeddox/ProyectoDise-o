from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100)
    correo_electronico = models.EmailField()
    contrasena = models.CharField(max_length=100)


class Maquinaria(models.Model):
    n_serie = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100) 
    capacidad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    img = models.CharField(max_length=500)