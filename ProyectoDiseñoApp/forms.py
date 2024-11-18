from django import forms

from ProyectoDiseñoApp.models import RegistrarUsuario
from ProyectoDiseñoApp.models import Maquinaria
from ProyectoDiseñoApp.models import Usuario
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={ 
                'class': 'form-control',
                'placeholder': '*****'
            }
        )
    )

    class Meta:
        model = Usuario
        fields = ['email', 'password']

class FormRegistrarUsuario(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su nombre'
        })
    )
    segundo_nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su segundo nombre'
        })
    )
    apellido = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su apellido'
        })
    )
    segundo_apellido = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su segundo apellido'
        })
    )
    correo_electronico = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '********'
        })
    )

    class Meta:
        model = RegistrarUsuario
        fields = ['nombre', 'segundo_nombre', 'apellido', 'segundo_apellido', 'correo_electronico', 'contrasena']

class FormMaquinaria(forms.ModelForm):
    class Meta:
        model = Maquinaria
        fields = '__all__'

class FormActualizarMaquinaria(forms.ModelForm):
    class Meta:
        model = Maquinaria
        fields = ['modelo', 'tipo', 'capacidad']