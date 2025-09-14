"""
Configuración del panel de administración para la aplicación 'roles'.

Este módulo registra y personaliza la visualización del modelo Profile
dentro del admin de Django. A través de esta configuración se definen:

- Las columnas que se muestran en la lista principal (usuario y rol).
- Los filtros laterales disponibles (por rol).
- Los campos de búsqueda habilitados (username y email del usuario).

De esta forma, el administrador puede gestionar de manera eficiente
los perfiles de usuario y sus roles en el sistema.
"""


from django.contrib import admin
from .models import Profile


# Registramos el modelo Profile en el admin de Django
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Mostramos estas columnas en la lista del admin
    list_display  = ("user", "role")
    # Permitimos filtrar por rol en el panel lateral
    list_filter   = ("role",)
    # Habilitamos búsqueda por username y email del usuario relacionado
    search_fields = ("user__username", "user__email")
