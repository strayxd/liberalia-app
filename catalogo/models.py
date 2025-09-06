# Modelo LibroFicha solo para probar la aplicación 
# luego hay que agregar el resto de los campos asociados a la ficha del libro
# -----------------
# Representa un libro registrado en el sistema.
# Cada libro tiene:
#   - ISBN único
#   - Título y autor
#   - Editorial asociada (relación con el modelo Editorial)
#   - Fecha de edición (opcional)
# 
# Los libros se ordenan por título de forma predeterminada.
# La representación (__str__) muestra "ISBN · Título" para facilitar la identificación en admin y consultas.


from django.db import models
from roles.models import Editorial  # Importamos el modelo Editorial para relacionarlo con LibroFicha

class LibroFicha(models.Model):
    isbn = models.CharField(max_length=32, unique=True)  # Código ISBN, único para cada libro
    titulo = models.CharField(max_length=255)  # Título del libro
    autor = models.CharField(max_length=255, blank=True)  # Autor del libro (puede quedar vacío)
    editorial = models.ForeignKey(  # Relación con la editorial (una editorial puede tener muchos libros)
        Editorial,
        on_delete=models.CASCADE,   # Si se elimina la editorial, se eliminan también sus libros
        related_name="libros"       # Nombre para acceder a los libros desde Editorial (ej: editorial.libros.all())
    )
    fecha_edicion = models.DateField(null=True, blank=True)  # Fecha de edición (puede quedar vacía)

    class Meta:
        ordering = ["titulo"]  # Ordenar resultados por título al hacer consultas

    def __str__(self):
        return f"{self.isbn} · {self.titulo}"  # Representación legible del objeto (ISBN + título)