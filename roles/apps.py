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
