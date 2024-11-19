from django import forms

from ProyectoDiseñoApp.models import RegistrarUsuario
from ProyectoDiseñoApp.models import Maquinaria
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

#Login
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )

# Registrar Usuario
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
    confirmar_contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme su contraseña'
        })
    )

    class Meta:
        model = RegistrarUsuario  # Relaciona este formulario con el modelo
        fields = ['nombre', 'segundo_nombre', 'apellido', 'segundo_apellido', 'correo_electronico', 'contrasena']

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get('contrasena')
        confirmar_contrasena = cleaned_data.get('confirmar_contrasena')

        if contrasena != confirmar_contrasena:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        return cleaned_data

    def clean_correo_electronico(self):
        correo = self.cleaned_data.get('correo_electronico')
        if RegistrarUsuario.objects.filter(correo_electronico=correo).exists():
            raise forms.ValidationError("El correo ya está registrado.")
        return correo


class FormRegistrarMaquinaria(forms.ModelForm):
    class Meta:
        model = Maquinaria
        fields = ['n_serie', 'modelo', 'tipo', 'capacidad', 'estado', 'img']
        widgets = {
            'n_serie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número de serie'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el modelo'
            }),
            'tipo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el tipo'
            }),
            'capacidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la capacidad'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el estado'
            }),
            'img': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subir una imagen'
            }),
        }


class FormActualizarMaquinaria(forms.ModelForm):
    class Meta:
        model = Maquinaria
        fields = ['modelo', 'tipo', 'capacidad', 'estado']
        widgets = {
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo'}),
            'capacidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Capacidad'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado'}),
        }