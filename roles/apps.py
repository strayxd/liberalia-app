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


# -----------------------------------------------------------------------------
# AppConfig: registra las señales al iniciar la app.
# -----------------------------------------------------------------------------
from django.apps import AppConfig

class RolesConfig(AppConfig):
    # Definimos el tipo de clave primaria por defecto
    default_auto_field = "django.db.models.BigAutoField"
    # Especificamos el nombre de la aplicación
    name = "roles"

    def ready(self):
        # Importamos las señales cuando la app está lista.
        # De esta manera garantizamos que al crear un usuario se genere automáticamente su Profile.
        import roles.signals  
