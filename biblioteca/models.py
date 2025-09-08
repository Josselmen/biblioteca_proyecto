from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name_plural = "Usuarios"

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorías"

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_publicacion = models.DateField()
    ejemplares_totales = models.PositiveIntegerField(default=1)
    ejemplares_disponibles = models.PositiveIntegerField(default=1)
    descripcion = models.TextField(blank=True)
    fecha_agregado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.titulo} - {self.autor}"

    @property
    def esta_disponible(self):
        return self.ejemplares_disponibles > 0

    class Meta:
        verbose_name_plural = "Libros"

class Prestamo(models.Model):
    ESTADO_CHOICES = [
        ('prestado', 'Prestado'),
        ('devuelto', 'Devuelto'),
        ('vencido', 'Vencido'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(default=timezone.now)
    fecha_devolucion_esperada = models.DateField()
    fecha_devolucion_real = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='prestado')
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.libro.titulo} - {self.usuario.nombre} {self.usuario.apellido}"

    @property
    def esta_vencido(self):
        if self.estado == 'devuelto':
            return False
        return timezone.now().date() > self.fecha_devolucion_esperada

    def save(self, *args, **kwargs):
        # Actualizar disponibilidad del libro al crear/modificar préstamo
        if self.pk is None:  # Nuevo préstamo
            if self.libro.ejemplares_disponibles > 0:
                self.libro.ejemplares_disponibles -= 1
                self.libro.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Préstamos"