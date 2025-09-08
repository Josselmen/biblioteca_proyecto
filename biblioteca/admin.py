from django.contrib import admin
from .models import Libro, Usuario, Prestamo, Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'categoria', 'ejemplares_totales', 'ejemplares_disponibles', 'fecha_agregado']
    list_filter = ['categoria', 'fecha_publicacion', 'fecha_agregado']
    search_fields = ['titulo', 'autor', 'isbn']
    date_hierarchy = 'fecha_agregado'

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'email', 'telefono', 'activo', 'fecha_registro']
    list_filter = ['activo', 'fecha_registro']
    search_fields = ['nombre', 'apellido', 'email']
    date_hierarchy = 'fecha_registro'

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ['libro', 'usuario', 'fecha_prestamo', 'fecha_devolucion_esperada', 'fecha_devolucion_real', 'estado']
    list_filter = ['estado', 'fecha_prestamo', 'fecha_devolucion_esperada']
    search_fields = ['libro__titulo', 'usuario__nombre', 'usuario__apellido']
    date_hierarchy = 'fecha_prestamo'