from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ProyectoDiseñoApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home),
    path('RegistrarUsuario/', views.RegistrarUsuarioView),
    path('Principal/', views.PaginaPrincipal),
    path('Inventario/', views.Inventario),
    path('Reporte/', views.Reporte),
    path('RegistrarM/', views.RegistrarM),
    path('Opciones/', views.Opciones),
    path('Actualizar/', views.ActualizarM),
    path('Renta/', views.Renta)
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)