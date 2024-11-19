from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class RegistrarUsuario(models.Model):
    nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100, blank=True, null=True)
    correo_electronico = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)  # Se almacenará como hash
    is_admin = models.BooleanField(default=False)  # Diferencia entre administrador y usuario normal

    def save(self, *args, **kwargs):
        # Hashea la contraseña solo si no está hasheada
        if not self.contrasena.startswith('pbkdf2_sha256$'):
            self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        """Método para establecer una nueva contraseña."""
        self.contrasena = make_password(raw_password)


class Maquinaria(models.Model):
    n_serie = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100) 
    capacidad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    img = models.ImageField(upload_to='maquinarias/', blank=True, null=True)