from django import forms
from .models import Libro, Usuario, Prestamo, Categoria
from datetime import date, timedelta

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'isbn', 'categoria', 'fecha_publicacion', 
                 'ejemplares_totales', 'ejemplares_disponibles', 'descripcion']
        widgets = {
            'fecha_publicacion': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'telefono']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['usuario', 'libro', 'fecha_devolucion_esperada', 'observaciones']
        widgets = {
            'fecha_devolucion_esperada': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar libros disponibles
        self.fields['libro'].queryset = Libro.objects.filter(ejemplares_disponibles__gt=0)
        # Solo mostrar usuarios activos
        self.fields['usuario'].queryset = Usuario.objects.filter(activo=True)
        
        # Establecer fecha por defecto (15 días desde hoy)
        if not self.instance.pk:
            self.fields['fecha_devolucion_esperada'].initial = date.today() + timedelta(days=15)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})