from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.template.loader import render_to_string
from xhtml2pdf import pisa #pip install xhtml2pdf
from django.contrib import messages
from django.db.models import Q
from ProyectoDiseñoApp.models import RegistrarUsuario, Maquinaria, Renta
from ProyectoDiseñoApp.forms import FormRegistrarUsuario, FormRegistrarMaquinaria, FormActualizarMaquinaria, LoginForm, RentarMaquinariaForm


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
    # Obtener conteos de estados de maquinaria desde la base de datos
    total_disponible = Maquinaria.objects.filter(estado='Disponible').count()
    total_rentada = Maquinaria.objects.filter(estado='Rentada').count()
    total_mantenimiento = Maquinaria.objects.filter(estado='En mantenimiento').count()
    total_fuera_servicio = Maquinaria.objects.filter(estado='Fuera de servicio').count()

    # Pasar datos al contexto
    context = {
        'disponible': total_disponible,
        'rentada': total_rentada,
        'en_mantenimiento': total_mantenimiento,
        'fuera_de_servicio': total_fuera_servicio
    }
    return render(request, 'index.html', context)

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
    # Datos para el gráfico
    total_disponible = Maquinaria.objects.filter(estado='Disponible').count()
    total_rentada = Maquinaria.objects.filter(estado='Rentada').count()
    total_mantenimiento = Maquinaria.objects.filter(estado='En mantenimiento').count()
    total_fuera_servicio = Maquinaria.objects.filter(estado='Fuera de servicio').count()

    # Historial de rentas
    rentas = Renta.objects.all()

    context = {
        'disponible': total_disponible,
        'rentada': total_rentada,
        'en_mantenimiento': total_mantenimiento,
        'fuera_de_servicio': total_fuera_servicio,
        'rentas': rentas,
    }
    return render(request, 'Reporte.html', context)

def RegistrarM(request):
    if request.method == 'POST':
        form = FormRegistrarMaquinaria(request.POST, request.FILES)  # Maneja datos y archivos
        if form.is_valid():
            maquinaria = form.save(commit=False)  # No guarda aún en la base de datos
            maquinaria.estado = 'Disponible'  # Asignar el estado predeterminado
            maquinaria.save()  # Guarda en la base de datos
            messages.success(request, 'Maquinaria registrada exitosamente.')
            return redirect('/Inventario/')  # Redirige al inventario
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = FormRegistrarMaquinaria()  # Formulario vacío para GET

    return render(request, 'RegistroMaquina.html', {'form': form})

def Opciones(request, id):
    maquinaria = get_object_or_404(Maquinaria, id=id)
    ultima_renta = maquinaria.rentas.last()

    if request.method == "POST":
        estado = request.POST.get("estado", maquinaria.estado)
        mantenimiento_info = request.POST.get("mantenimiento_info", "")

        maquinaria.estado = estado
        maquinaria.informacion_mantenimiento = mantenimiento_info
        maquinaria.save()

        # Redirigir siempre a Inventario
        return redirect('/Inventario/')

    return render(
        request,
        "opciones.html",
        {"maquinaria": maquinaria, "ultima_renta": ultima_renta},
    )
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


def RentarMaquinaria(request, id):
    maquinaria = get_object_or_404(Maquinaria, id=id)

    if request.method == "POST":
        form = RentarMaquinariaForm(request.POST)
        if form.is_valid():
            cliente = form.cleaned_data['cliente']
            fecha_rentado = form.cleaned_data['fecha_rentado']
            fecha_devolucion = form.cleaned_data['fecha_devolucion']

            # Verificar si ya existe una renta activa para este cliente y maquinaria
            renta_existente = Renta.objects.filter(
                maquinaria=maquinaria,
                cliente=cliente,
                fecha_devolucion__gte=fecha_rentado  # Verificar solapamiento en las fechas
            ).first()

            if renta_existente:
                # Actualizar las fechas en la renta existente
                renta_existente.fecha_rentado = fecha_rentado
                renta_existente.fecha_devolucion = fecha_devolucion
                renta_existente.save()
                messages.success(request, "La renta ha sido actualizada correctamente.")
            else:
                # Crear una nueva renta
                nueva_renta = form.save(commit=False)
                nueva_renta.maquinaria = maquinaria
                nueva_renta.save()
                messages.success(request, "La maquinaria ha sido rentada correctamente.")

            # Cambiar el estado de la maquinaria
            maquinaria.estado = "Rentada"
            maquinaria.save()

            return redirect(f"/Opciones/{id}/")
    else:
        form = RentarMaquinariaForm()

    return render(request, "renta.html", {"form": form, "maquinaria": maquinaria})

# Actualizar Maquinaria
def ActualizarM(request):
    maquinaria_id = request.GET.get('id')  # Obtiene el ID de la maquinaria desde la URL
    maquinaria = get_object_or_404(Maquinaria, id=maquinaria_id)  # Busca la maquinaria en la base de datos

    if request.method == 'POST':
        # Procesar el formulario enviado con datos y archivos
        form = FormActualizarMaquinaria(request.POST, instance=maquinaria)
        if form.is_valid():
            form.save()  # Guarda los cambios en la base de datos
            # Diferenciar la redirección según origen
            if request.GET.get('from') == 'inventario':
                return redirect('/Inventario/')
            else:
                messages.success(request, 'Datos actualizados exitosamente.')
                return redirect(f'/Actualizar/?id={maquinaria_id}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        # Inicializar el formulario con los datos de la maquinaria
        form = FormActualizarMaquinaria(instance=maquinaria)

    # Renderiza el formulario con los datos iniciales cargados
    return render(request, 'ActualizarMaquina.html', {'form': form, 'maquinaria': maquinaria})

def EliminarMaquinaria(request, id):
    maquinaria = get_object_or_404(Maquinaria, id=id)  # Busca la maquinaria en la base de datos
    maquinaria.delete()  # Elimina la maquinaria
    messages.success(request, "La maquinaria ha sido eliminada correctamente.")
    return redirect('/Inventario/')  # Redirige al inventario después de eliminar

def ActualizarUsuario(request, id):
    usuario = get_object_or_404(RegistrarUsuario, id=id)

    if request.method == "POST":
        form = FormRegistrarUsuario(request.POST, instance=usuario)
        if form.is_valid():
            # Evita la validación del correo duplicado si el correo no cambia
            if form.cleaned_data['correo_electronico'] == usuario.correo_electronico:
                usuario.nombre = form.cleaned_data['nombre']
                usuario.segundo_nombre = form.cleaned_data['segundo_nombre']
                usuario.apellido = form.cleaned_data['apellido']
                usuario.segundo_apellido = form.cleaned_data['segundo_apellido']
                usuario.contrasena = form.cleaned_data['contrasena']
                usuario.save()
            else:
                form.save()  # Permite actualizar si cambia el correo electrónico

            messages.success(request, "Usuario actualizado correctamente.")
            return redirect("/RegistrarUsuario/")
        else:
            messages.error(request, "Ocurrió un error al actualizar el usuario.")
    else:
        form = FormRegistrarUsuario(instance=usuario)

    return render(request, "registroUsuario.html", {"form": form, "actualizar": True, "usuarios": RegistrarUsuario.objects.filter(is_admin=False)})

def EliminarUsuario(request, id):
    usuario = get_object_or_404(RegistrarUsuario, id=id)

    # Asegurarse de no eliminar al admin
    if usuario.is_admin:
        messages.error(request, "No puedes eliminar al administrador.")
        return redirect("/RegistrarUsuario/")

    # Eliminar el usuario si no es admin
    usuario.delete()
    messages.success(request, "Usuario eliminado correctamente.")
    return redirect("/RegistrarUsuario/")


def generar_pdf(request):
    context = {
        "disponible": Maquinaria.objects.filter(estado="Disponible").count(),
        "rentada": Maquinaria.objects.filter(estado="Rentada").count(),
        "en_mantenimiento": Maquinaria.objects.filter(estado="En mantenimiento").count(),
        "fuera_de_servicio": Maquinaria.objects.filter(estado="Fuera de servicio").count(),
        "rentas": Renta.objects.all(),
        "pdf": True,  # Variable para identificar el contexto del PDF
    }
    html = render_to_string("Reporte.html", context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=Reporte_Maquinaria.pdf"
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=400)
    return response