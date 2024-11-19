from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from django.db.models import Q
from ProyectoDiseñoApp.models import RegistrarUsuario, Maquinaria
from ProyectoDiseñoApp.forms import FormRegistrarUsuario, FormRegistrarMaquinaria, FormActualizarMaquinaria, LoginForm


# Create your views here.
def Home(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Depuración: Imprimir los datos ingresados
            print(f"Correo ingresado: {email}")
            print(f"Contraseña ingresada: {password}")

            # Busca al usuario en la base de datos
            user = RegistrarUsuario.objects.filter(correo_electronico=email).first()

            # Depuración: Imprimir resultados de la consulta y validación
            if user:
                print(f"Usuario encontrado: {user.correo_electronico}")
                print(f"Contraseña válida: {check_password(password, user.contrasena)}")
            else:
                print("Usuario no encontrado.")

            # Lógica para verificar credenciales y redirigir
            if user:
                if check_password(password, user.contrasena):
                    if user.is_admin:
                        return redirect('/RegistrarUsuario/')
                    else:
                        return redirect('/Principal/')
                else:
                    return render(request, 'IniciarSesion.html', {
                        'form': form,
                        'error': 'Contraseña incorrecta.'
                    })
            else:
                return render(request, 'IniciarSesion.html', {
                    'form': form,
                    'error': 'El usuario no existe.'
                })
    else:
        form = LoginForm()

    return render(request, 'IniciarSesion.html', {'form': form})

def PaginaPrincipal(request):
    if request.method == "POST":
        if "actualizar_datos" in request.POST:  # Botón para "Actualizar Datos"
            request.session['allow_update'] = True
            return redirect('/Inventario/')
        if "ver_inventario" in request.POST:  # Botón para "Inventario"
            request.session['allow_update'] = False
            return redirect('/Inventario/')
    return render(request, 'index.html')

def Inventario(request):
    # Capturamos el parámetro "modo" de la URL
    modo = request.GET.get('modo', 'ver_inventario')  # Por defecto, es "ver_inventario"
    
    query = request.GET.get('q', '')  # Captura el valor ingresado en la barra de búsqueda
    if query:
        maquinarias = Maquinaria.objects.filter(
            Q(n_serie__icontains=query) | 
            Q(modelo__icontains=query) | 
            Q(estado__icontains=query)
        )
    else:
        maquinarias = Maquinaria.objects.all()  # Si no hay búsqueda, muestra todas las maquinarias

    # Renderiza el inventario con el modo pasado
    return render(request, 'Inventario.html', {'maquinarias': maquinarias, 'query': query, 'modo': modo})

def Reporte(request):
    data = {}
    return render(request, 'Reporte.html', data)

def RegistrarM(request):
    if request.method == 'POST':
        form = FormRegistrarMaquinaria(request.POST, request.FILES)  # Maneja datos y archivos
        if form.is_valid():
            form.save()  # Guarda la maquinaria directamente en la base de datos
            messages.success(request, 'Maquinaria registrada exitosamente.')
            return redirect('/Inventario/')  # Redirige al inventario
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = FormRegistrarMaquinaria()  # Formulario vacío para GET

    return render(request, 'RegistroMaquina.html', {'form': form})

def Opciones(request):
    data = {}
    return render(request, 'opciones.html', data)

def RegistrarUsuarioView(request):
    if request.method == 'POST':
        form = FormRegistrarUsuario(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado exitosamente.')
            form = FormRegistrarUsuario()  # Resetea el formulario después del registro
    else:
        form = FormRegistrarUsuario()

    # Filtra solo los usuarios normales (is_admin=False)
    usuarios_normales = RegistrarUsuario.objects.filter(is_admin=False)

    context = {
        'form': form,
        'usuarios': usuarios_normales,  # Pasa los usuarios al template
    }

    return render(request, 'registroUsuario.html', context)


def Renta(request):
    data = {}
    return render(request, 'renta.html', data)

# Actualizar Maquinaria
def ActualizarM(request):
    maquinaria_id = request.GET.get('id')  # Obtiene el ID de la maquinaria desde la URL
    maquinaria = Maquinaria.objects.get(id=maquinaria_id)  # Busca la maquinaria en la base de datos

    if request.method == 'POST':
        # Procesar el formulario enviado
        maquinaria.modelo = request.POST.get('modelo')
        maquinaria.tipo = request.POST.get('tipo')
        maquinaria.capacidad = request.POST.get('capacidad')
        maquinaria.estado = request.POST.get('estado')
        maquinaria.save()  # Guarda los cambios en la base de datos
        messages.success(request, 'Datos actualizados exitosamente.')
        return redirect('/Inventario/')  # Redirige al inventario después de actualizar

    # Renderiza el formulario con los datos de la maquinaria
    return render(request, 'ActualizarMaquina.html', {'maquinaria': maquinaria})