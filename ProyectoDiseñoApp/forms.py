from datetime import date
from django import forms
from ProyectoDiseñoApp.models import RegistrarUsuario
from ProyectoDiseñoApp.models import Maquinaria
from ProyectoDiseñoApp.models import Renta
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
        model = RegistrarUsuario
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
        usuario_id = self.instance.id  # Excluir el usuario actual de la validación
        
        if RegistrarUsuario.objects.filter(correo_electronico=correo).exclude(id=usuario_id).exists():
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
        


class RentarMaquinariaForm(forms.ModelForm):
    terms = forms.BooleanField(
        label="Acepto los términos y condiciones de la RENTA",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = Renta
        fields = ['cliente', 'fecha_rentado', 'fecha_devolucion']
        widgets = {
            'cliente': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'fecha_rentado': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'fecha_devolucion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }
        labels = {
            'cliente': 'Cliente',
            'fecha_rentado': 'Fecha de rentado',
            'fecha_devolucion': 'Fecha de devolución',
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_rentado = cleaned_data.get('fecha_rentado')
        fecha_devolucion = cleaned_data.get('fecha_devolucion')

        # Validación: Fecha de rentado no puede ser anterior al día actual
        if fecha_rentado and fecha_rentado < date.today():
            raise forms.ValidationError({
                'fecha_rentado': 'La fecha de rentado no puede ser anterior al día de hoy.'
            })

        # Validación: Fecha de devolución debe ser mayor o igual a la fecha de rentado
        if fecha_rentado and fecha_devolucion and fecha_devolucion < fecha_rentado:
            raise forms.ValidationError({
                'fecha_devolucion': 'La fecha de devolución no puede ser anterior a la fecha de rentado.'
            })

        return cleaned_data