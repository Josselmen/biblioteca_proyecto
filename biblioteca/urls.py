from django.urls import path
from . import views

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),
    
    # URLs de libros
    path('libros/', views.lista_libros, name='lista_libros'),
    path('libros/agregar/', views.agregar_libro, name='agregar_libro'),
    path('libros/<int:libro_id>/', views.detalle_libro, name='detalle_libro'),
    path('libros/<int:libro_id>/eliminar/', views.eliminar_libro, name='eliminar_libro'),
    

    
    # URLs de usuarios
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/agregar/', views.agregar_usuario, name='agregar_usuario'),
    path('usuarios/<int:usuario_id>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    
    # URLs de préstamos
    path('prestamos/', views.lista_prestamos, name='lista_prestamos'),
    path('prestamos/agregar/', views.agregar_prestamo, name='agregar_prestamo'),
    path('prestamos/<int:prestamo_id>/devolver/', views.devolver_libro, name='devolver_libro'),
    
    # URLs de categorías
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/agregar/', views.agregar_categoria, name='agregar_categoria'),
    
    # Reportes
    path('reportes/', views.reportes, name='reportes'),
]