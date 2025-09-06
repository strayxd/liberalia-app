# -------------------------------------------------------------------------------
# Rutas (URLs) de la app "roles":
# - Define los paneles de usuario según el rol (ADMIN, EDITOR, CONSULTOR).
# - Incluye vistas para crear y editar libros desde el panel del editor.
# -------------------------------------------------------------------------------


from django.urls import path
from .views import (
    PanelAdminView, PanelConsultorView, PanelEditorView,
    LibroCreateView, LibroEditView
)

app_name = "roles"

urlpatterns = [
    path("admin/",      PanelAdminView.as_view(),      name="panel_admin"),
    path("consultor/",  PanelConsultorView.as_view(),  name="panel_consultor"),
    path("editor/",     PanelEditorView.as_view(),     name="panel_editor"),

    # Editor: crear/editar (stubs)
    path("editor/fichas/nueva/",        LibroCreateView.as_view(), name="ficha_new"),
    path("editor/fichas/<str:isbn>/",   LibroEditView.as_view(),   name="ficha_edit"),
]
