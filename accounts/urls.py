from django.urls import path
from .views import LoginView, logout_view  

# Definimos el namespace de la app para poder referirnos a sus URLs de forma explícita
app_name = 'accounts'

# Listado de rutas de la app 'accounts'
urlpatterns = [
    # Ruta para iniciar sesión: usamos la vista basada en clases LoginView
    # Podemos referirnos a esta URL como 'accounts:login'
    path('login/', LoginView.as_view(), name='login'),

    # Ruta para cerrar sesión: usamos la función logout_view
    # Podemos referirnos a esta URL como 'accounts:logout'
    path('logout/', logout_view, name='logout'),
]