"""
Definición de rutas (URLs) para la aplicación 'accounts'.

Este módulo centraliza las URLs relacionadas con la autenticación y gestión
básica de usuarios dentro del sistema. Incluye:

- Login: acceso mediante correo electrónico y contraseña.
- Logout: cierre de sesión del usuario autenticado.
- Cambio de contraseña: flujo para actualizar la contraseña desde la cuenta activa.

El uso del atributo 'app_name' permite referirse a estas rutas de manera
explícita con el prefijo 'accounts:', facilitando su reutilización en
plantillas, redirecciones y vistas.
"""

from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import LoginView, logout_view, home

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


    # --- NUEVO: cambio de contraseña para usuario autenticado ---
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/password_change_form.html",
            success_url=reverse_lazy("accounts:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html",
        ),
        name="password_change_done",
    ),
]