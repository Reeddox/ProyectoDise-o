from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Usuario(AbstractUser):
    email = models.EmailField('Correo Electrónico', unique=True)
    password = models.CharField('Contraseña', max_length=128)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['id']

    def __str__(self):
        return self.email

class RegistrarUsuario(models.Model):
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