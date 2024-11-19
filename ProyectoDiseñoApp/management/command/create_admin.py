from django.core.management.base import BaseCommand
from ProyectoDiseñoApp.models import RegistrarUsuario

class Command(BaseCommand):
    help = "Crea un administrador por defecto si no existe"

    def handle(self, *args, **kwargs):
        if not RegistrarUsuario.objects.filter(correo_electronico="admin@example.com").exists():
            RegistrarUsuario.objects.create(
                nombre="Admin",
                apellido="User",
                correo_electronico="admin@example.com",
                contrasena="adminpassword",  # La contraseña será cifrada automáticamente si tu modelo la hashea
                is_admin=True,
            )
            self.stdout.write("Administrador creado con éxito.")
        else:
            self.stdout.write("El administrador ya existe.")
