from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from ProyectoDiseñoApp.models import Usuario, RegistrarUsuario,Maquinaria
from ProyectoDiseñoApp.forms import FormRegistrarUsuario, FormMaquinaria, FormActualizarMaquinaria, LoginForm

# Create your views here.

def Home(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('')  # Cambia 'home' por tu URL
    return render(request, 'IniciarSesion.html', {'form': form})

def PaginaPrincipal(request):
    data = {}
    return render(request, 'index.html', data)

def Inventario(request):
    data = {}
    return render(request, 'Inventario.html', data)

def Reporte(request):
    data = {}
    return render(request, 'Reporte.html', data)

def RegistrarM(request):
    data = {}
    return render(request, 'RegistroMaquina.html', data)

def Opciones(request):
    data = {}
    return render(request, 'opciones.html', data)

usuarios_ejemplo = [
        {
            'nombre': 'Juan',
            'segundo_nombre': 'Carlos',
            'apellido': 'Pérez',
            'segundo_apellido': 'García',
            'correo_electronico': 'Usuario@gmail.com'
        }
    ]

def RegistrarUsuario(request):
    if request.method == 'POST':
        form = FormRegistrarUsuario(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado exitosamente')
            # Crear un nuevo formulario vacío
            form = FormRegistrarUsuario()
    else:
        form = FormRegistrarUsuario()
    return render(request, 'registro.html', {'form': form})

def Renta(request):
    data = {}
    return render(request, 'renta.html', data)

def ActualizarM(request):
    form = FormActualizarMaquinaria()
    if request.method == 'POST':
        form = FormActualizarMaquinaria(request.POST)
        if form.is_valid():
            form.save()
        return 
    data = {'form' : form}
    return render(request, 'ActualizarMaquina.html', data)