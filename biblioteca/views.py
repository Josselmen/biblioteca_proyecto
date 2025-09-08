from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from .models import Libro, Usuario, Prestamo, Categoria
from .forms import LibroForm, UsuarioForm, PrestamoForm, CategoriaForm

def index(request):
    total_libros = Libro.objects.count()
    total_usuarios = Usuario.objects.filter(activo=True).count()
    prestamos_activos = Prestamo.objects.filter(estado='prestado').count()
    prestamos_vencidos = Prestamo.objects.filter(
        estado='prestado', 
        fecha_devolucion_esperada__lt=timezone.now().date()
    ).count()
    
    context = {
        'total_libros': total_libros,
        'total_usuarios': total_usuarios,
        'prestamos_activos': prestamos_activos,
        'prestamos_vencidos': prestamos_vencidos,
    }
    return render(request, 'index.html', context)

# VISTAS DE LIBROS
def lista_libros(request):
    libros = Libro.objects.select_related('categoria').all()
    categorias = Categoria.objects.all()
    
    # Filtro por categoría
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        libros = libros.filter(categoria_id=categoria_id)
    
    # Búsqueda
    busqueda = request.GET.get('buscar')
    if busqueda:
        libros = libros.filter(
            Q(titulo__icontains=busqueda) |
            Q(autor__icontains=busqueda) |
            Q(isbn__icontains=busqueda)
        )
    
    context = {
        'libros': libros,
        'categorias': categorias,
        'categoria_seleccionada': int(categoria_id) if categoria_id else None,
        'busqueda': busqueda or '',
    }
    return render(request, 'libros/lista.html', context)

def agregar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Libro agregado exitosamente.')
            return redirect('lista_libros')
    else:
        form = LibroForm()
    return render(request, 'libros/agregar.html', {'form': form})

def detalle_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    prestamos = Prestamo.objects.filter(libro=libro).select_related('usuario').order_by('-fecha_prestamo')[:10]
    return render(request, 'libros/detalle.html', {'libro': libro, 'prestamos': prestamos})

def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if Prestamo.objects.filter(libro=libro, estado='prestado').exists():
        messages.error(request, 'No se puede eliminar el libro porque tiene préstamos activos.')
    else:
        libro.delete()
        messages.success(request, 'Libro eliminado exitosamente.')
    return redirect('lista_libros')

# VISTAS DE USUARIOS
def lista_usuarios(request):
    usuarios = Usuario.objects.annotate(
        prestamos_activos=Count('prestamo', filter=Q(prestamo__estado='prestado'))
    ).all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

def agregar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario agregado exitosamente.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/agregar.html', {'form': form})

def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if Prestamo.objects.filter(usuario=usuario, estado='prestado').exists():
        messages.error(request, 'No se puede eliminar el usuario porque tiene préstamos activos.')
    else:
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
    return redirect('lista_usuarios')

# VISTAS DE PRÉSTAMOS
def lista_prestamos(request):
    prestamos = Prestamo.objects.select_related('usuario', 'libro').all().order_by('-fecha_prestamo')
    
    # Filtro por estado
    estado = request.GET.get('estado')
    if estado:
        prestamos = prestamos.filter(estado=estado)
    
    return render(request, 'prestamos/lista.html', {
        'prestamos': prestamos,
        'estado_seleccionado': estado
    })

def agregar_prestamo(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Préstamo registrado exitosamente.')
            return redirect('lista_prestamos')
    else:
        form = PrestamoForm()
    return render(request, 'prestamos/agregar.html', {'form': form})

def devolver_libro(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    if prestamo.estado == 'prestado':
        prestamo.estado = 'devuelto'
        prestamo.fecha_devolucion_real = timezone.now()
        prestamo.save()
        
        # Aumentar ejemplares disponibles
        prestamo.libro.ejemplares_disponibles += 1
        prestamo.libro.save()
        
        messages.success(request, 'Libro devuelto exitosamente.')
    else:
        messages.error(request, 'Este libro ya fue devuelto.')
    return redirect('lista_prestamos')

# VISTAS DE CATEGORÍAS
def lista_categorias(request):
    categorias = Categoria.objects.annotate(
        total_libros=Count('libro')
    ).all()
    return render(request, 'categorias/lista.html', {'categorias': categorias})

def agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría agregada exitosamente.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/agregar.html', {'form': form})

def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if Libro.objects.filter(categoria=categoria).exists():
        messages.error(request, 'No se puede eliminar la categoría porque tiene libros asociados.')
    else:
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
    return redirect('lista_categorias')

# VISTAS DE REPORTES
def reportes(request):
    # Estadísticas generales
    total_libros = Libro.objects.count()
    total_usuarios = Usuario.objects.count()
    total_prestamos = Prestamo.objects.count()
    prestamos_activos = Prestamo.objects.filter(estado='prestado').count()
    prestamos_vencidos = Prestamo.objects.filter(
        estado='prestado',
        fecha_devolucion_esperada__lt=timezone.now().date()
    ).count()
    
    # Libros más prestados
    libros_populares = Libro.objects.annotate(
        total_prestamos=Count('prestamo')
    ).filter(total_prestamos__gt=0).order_by('-total_prestamos')[:10]
    
    # Usuarios más activos
    usuarios_activos = Usuario.objects.annotate(
        total_prestamos=Count('prestamo')
    ).filter(total_prestamos__gt=0).order_by('-total_prestamos')[:10]
    
    context = {
        'total_libros': total_libros,
        'total_usuarios': total_usuarios,
        'total_prestamos': total_prestamos,
        'prestamos_activos': prestamos_activos,
        'prestamos_vencidos': prestamos_vencidos,
        'libros_populares': libros_populares,
        'usuarios_activos': usuarios_activos,
    }
    return render(request, 'reportes.html', context)