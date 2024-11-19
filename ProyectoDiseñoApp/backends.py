from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import RegistrarUsuario

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = RegistrarUsuario.objects.get(correo_electronico=email)
            if check_password(password, user.contrasena):
                return user
        except RegistrarUsuario.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            return RegistrarUsuario.objects.get(pk=user_id)
        except RegistrarUsuario.DoesNotExist:
            return None
