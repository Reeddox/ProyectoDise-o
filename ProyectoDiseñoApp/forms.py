from django import forms

from ProyectoDiseñoApp.models import Usuario
from ProyectoDiseñoApp.models import Maquinaria


class FormUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'

class FormMaquinaria(forms.ModelForm):
    class Meta:
        model = Maquinaria
        fields = '__all__'

class FormActualizarMaquinaria(forms.ModelForm):
    class Meta:
        model = Maquinaria
        fields = ['modelo', 'tipo', 'capacidad']