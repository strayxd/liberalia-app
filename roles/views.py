# -----------------------------------------------------------------------------
# Tres paneles por rol. Usamos un decorador sencillo para exigir el rol esperado.
# Si no coincide, redirige (ajusta 'home-root' por la vista que prefieras).
# -----------------------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile


def _role(user):
    """Devuelve el rol del usuario o None si no tiene profile."""
    # Aquí lo que hacemos es usar getattr de forma encadenada para evitar errores
    # en caso de que el usuario no tenga profile asociado.
    # Si existe user.profile.role lo devolvemos, si no, retornamos None.
    return getattr(getattr(user, "profile", None), "role", None)


def role_required(expected_role):
    """
    Decorador que exige:
      - estar autenticado
      - tener el rol 'expected_role'
    """
    # Definimos un decorador que envolverá la vista original.
    def decorator(viewfunc):
        @login_required
        def _wrapped(request, *args, **kwargs):
            if _role(request.user) != expected_role:
                return redirect("home-root")  # cámbialo por 403 si prefieres
            return viewfunc(request, *args, **kwargs)
        return _wrapped
    return decorator


@role_required(Profile.ROLE_ADMIN)
def panel_admin(request):
    # En este panel construimos el contexto con el usuario y su rol
    ctx = {"user_obj": request.user, "role": request.user.profile.role}
    # Renderizamos la plantilla específica para el panel de administrador
    return render(request, "roles/panel_admin.html", ctx)


@role_required(Profile.ROLE_EDITOR)
def panel_editor(request):
    # Aquí hacemos lo mismo, pero para el rol de editor
    ctx = {"user_obj": request.user, "role": request.user.profile.role}
    return render(request, "roles/panel_editor.html", ctx)


@role_required(Profile.ROLE_CONSULTOR)
def panel_consultor(request):
    # Y en este caso repetimos la lógica, pero para el rol de consultor
    ctx = {"user_obj": request.user, "role": request.user.profile.role}
    return render(request, "roles/panel_consultor.html", ctx)
