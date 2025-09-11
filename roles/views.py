from __future__ import annotations
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views import View

from .models import Profile, UsuarioEditorial
from catalogo.models import LibroFicha

import csv
from datetime import datetime


# ----------------------------
# Helpers de rol
# ----------------------------
def _role(user):
    """Devuelve el rol del usuario o None si no tiene profile."""
    return getattr(getattr(user, "profile", None), "role", None)


def role_required(expected_role):
    """Decorador que exige login y rol esperado."""
    def decorator(viewfunc):
        @login_required
        def _wrapped(request, *args, **kwargs):
            if _role(request.user) != expected_role:
                return redirect("home-root")  
            return viewfunc(request, *args, **kwargs)
        return _wrapped
    return decorator


def _panel_flags(user):
    """
    Construye las banderas de UI / capacidades por rol para el template unificado.
    """
    role = _role(user)
    is_admin = role == Profile.ROLE_ADMIN
    is_editor = role == Profile.ROLE_EDITOR
    is_consultor = role == Profile.ROLE_CONSULTOR

    if is_admin:
        role_label = "ADMIN"
        role_badge_class = "bg-danger"
    elif is_editor:
        role_label = "EDITOR"
        role_badge_class = "bg-secondary"
    else:
        role_label = "CONSULTOR"
        role_badge_class = "bg-secondary"

    return {
        "is_admin": is_admin,
        "role_label": role_label,
        "role_badge_class": role_badge_class,

        # Capacidades por rol (alineadas a plantillas originales)
        "can_download": is_admin or is_consultor,  # Admin/Consultor tenían "Descargar"
        "can_create": is_editor,                   # Editor tenía "Crear"
        "can_edit": is_editor,                     # Editor tenía "Editar"
        "show_detail": is_admin or is_consultor,   # Admin/Consultor mostraban "Detalle"
        "detail_disabled": "disabled",

        # Nombres de URL 
        # (IMPORTANTE: CAMBIAR POSTERIORMENTE CON LOS NOMBRES REALES)
        "create_url_name": "roles:ficha_new" if is_editor else None,
        "edit_url_name": "roles:ficha_edit" if is_editor else None,
    }


# ----------------------------
# Utils de filtrado/ordenación
# ----------------------------
ALLOWED_SORTS = {
    "isbn": "isbn",
    "titulo": "titulo",
    "autor": "autor",
    "editorial": "editorial__nombre",
    "fecha": "fecha_edicion",
}

def _parse_date(s: str | None):
    if not s:
        return None
    # <input type="date"> entrega 'YYYY-MM-DD'
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None

def build_queryset_for_user(user, params):
    """
    Construye un queryset de LibroFicha respetando:
    - Búsqueda por nombre de editorial (q)
    - Rango de fechas (date_from, date_to)
    - Límite por rol (editor ve solo sus editoriales)
    - Ordenamiento (?sort=)
    """
    qs = LibroFicha.objects.select_related("editorial")
    q = (params.get("q") or "").strip()
    date_from = _parse_date(params.get("date_from"))
    date_to   = _parse_date(params.get("date_to"))
    sort_key  = params.get("sort") or ""

    if q:
        qs = qs.filter(editorial__nombre__icontains=q)

    if date_from:
        qs = qs.filter(fecha_edicion__gte=date_from)
    if date_to:
        qs = qs.filter(fecha_edicion__lte=date_to)

    # Restricción por rol (EDITOR: solo sus editoriales)
    role = getattr(getattr(user, "profile", None), "role", None)
    if role == Profile.ROLE_EDITOR:
        ed_ids = UsuarioEditorial.objects.filter(user=user).values_list("editorial_id", flat=True)
        qs = qs.filter(editorial_id__in=list(ed_ids))

    # Orden
    if sort_key in ALLOWED_SORTS:
        qs = qs.order_by(ALLOWED_SORTS[sort_key])

    return qs


# ----------------------------
# Vistas de lista (template unificado PANEL.HTML)
# ----------------------------
class BasePanelView(LoginRequiredMixin, View):
    template_name = "roles/panel.html"   # TEMPLATE ÚNICO PARA LOS TRES TIPOS DE USUARIOS
    role_required = None                 # opcional 

    def get(self, request: HttpRequest):
        # Exportación CSV (solo si el rol lo permite)
        if request.GET.get("export") == "csv":
            role = getattr(getattr(request.user, "profile", None), "role", None)
            if self.role_required and role != self.role_required:
                return redirect("home-root")  # o HttpResponse("Prohibido", status=403)
            flags = _panel_flags(request.user)
            if not flags.get("can_download"):
                return HttpResponse("No autorizado", status=403)
            return self.export_csv(request)

        qs = build_queryset_for_user(request.user, request.GET)
        ctx = {
            "rows": qs[:1000],  # limitada a 1000 filas
            "q": request.GET.get("q", ""),
            "date_from": request.GET.get("date_from", ""),
            "date_to": request.GET.get("date_to", ""),
            "sort": request.GET.get("sort", ""),
            "ALLOWED_SORTS": ALLOWED_SORTS,
        }

        # valida rol si corresponde
        role = getattr(getattr(request.user, "profile", None), "role", None)
        if self.role_required and role != self.role_required:
            return redirect("home-root")  # o HttpResponse("Prohibido", status=403)

        # inyecta banderas por rol
        ctx.update(_panel_flags(request.user))
        return render(request, self.template_name, ctx)

    def export_csv(self, request: HttpRequest) -> HttpResponse:
        qs = build_queryset_for_user(request.user, request.GET)

        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="libros.csv"'
        writer = csv.writer(response)
        writer.writerow(["ISBN", "TÍTULO", "AUTOR", "EDITORIAL", "FECHA_EDICIÓN"])

        for r in qs:
            writer.writerow([
                r.isbn,
                r.titulo,
                r.autor,
                r.editorial.nombre,
                r.fecha_edicion.isoformat() if r.fecha_edicion else "",
            ])
        return response


class PanelAdminView(BasePanelView):
    role_required = Profile.ROLE_ADMIN


class PanelConsultorView(BasePanelView):
    role_required = Profile.ROLE_CONSULTOR


class PanelEditorView(BasePanelView):
    role_required = Profile.ROLE_EDITOR


# ----------------------------
# Vistas provisionales para crear/editar fichas (placeholders)
# ----------------------------
class LibroCreateView(LoginRequiredMixin, View):
    def get(self, request):
        # TODO: template de creación
        return HttpResponse("Nueva ficha (formulario)")


class LibroEditView(LoginRequiredMixin, View):
    def get(self, request, isbn):
        # TODO: template de edición
        return HttpResponse(f"Editar ficha {isbn}")
