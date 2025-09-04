from django.contrib import admin
from .models import Profile


# Registramos el modelo Profile en el admin de Django
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Mostramos estas columnas en la lista del admin
    list_display  = ("user", "role")
    # Permitimos filtrar por rol en el panel lateral
    list_filter   = ("role",)
    # Habilitamos búsqueda por username y email del usuario relacionado
    search_fields = ("user__username", "user__email")
