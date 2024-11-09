from django.shortcuts import render, redirect
from ProyectoDiseñoApp.models import Usuario, Maquinaria
from ProyectoDiseñoApp.forms import FormUsuario, FormMaquinaria, FormActualizarMaquinaria

# Create your views here.

def Home(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email == 'Usuario@gmail.com' and password == '123456':
            return redirect('/Principal/')
        elif email == 'Admin@gmail.com' and password == 'admin':
            return redirect('/RegistrarUsuario/')
        else:
            error_message = 'Correo electrónico o contraseña inválidos'
    else:
        error_message = ''
    
    return render(request, 'IniciarSesion.html', {'error_message': error_message})

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
    form = FormUsuario()
    if request.method == 'POST':
        form = FormUsuario(request.POST)
        if form.is_valid():
            form.save()
        return
    data = {'form' : form}
    return render(request, 'registroUsuario.html', data)

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