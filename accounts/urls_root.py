from django.urls import path
from .views import home 

# Definimos las rutas (URLs) de la app
urlpatterns = [
    # Ruta raíz de la aplicación: cuando el usuario entra a "/", llamamos a la vista 'home'
    # Le damos el nombre 'home-root' para poder referirnos a ella fácilmente con {% url 'home-root' %}
    path('', home, name='home-root'),
]