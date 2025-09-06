"""
Configuración de la aplicación 'catalogo'.

Este módulo define la clase de configuración usada por Django para
registrar la aplicación dentro del proyecto. En este caso se indica:

- El tipo de clave primaria por defecto (BigAutoField).
- El nombre interno de la app, que permite a Django reconocerla y
  enlazarla con sus modelos, vistas, formularios y rutas.

La aplicación 'catalogo' está destinada a gestionar los recursos
editoriales o productos del sistema, centralizando su administración
y organización dentro del proyecto.
"""


from django.apps import AppConfig


class CatalogoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalogo'
