
import os
from django.core.wsgi import get_wsgi_application

# --------------------------------------------------------------------------
# Configuramos la variable de entorno para que Django sepa qué settings usar
# --------------------------------------------------------------------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'liberalia.settings')


# --------------------------------------------------------------------------
# Creamos la aplicación WSGI que servirá la app en servidores como Gunicorn
# o uWSGI. Esto es el punto de entrada para el despliegue en producción.
# --------------------------------------------------------------------------
application = get_wsgi_application()
