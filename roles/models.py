# -----------------------------------------------------------------------------
# Estos modelos cubren tu diagrama:
#   - Editorial: catálogo de editoriales
#   - Profile: 1–1 con el usuario de Django; guarda el rol (ADMIN/EDITOR/CONSULTOR)
#   - UsuarioEditorial: relación M:N entre usuario y editorial (usuario puede
#     pertenecer a varias editoriales y viceversa)
# -----------------------------------------------------------------------------

from django.conf import settings
from django.db import models


class Editorial(models.Model):
    # Catálogo de editoriales (opcional para ahora; no interfiere con Opción A)
    nombre = models.CharField(max_length=150)
    id_fiscal = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Editorial"
        verbose_name_plural = "Editoriales"

    # Mostramos el nombre de la editorial en el admin y otros contextos
    def __str__(self) -> str:        
        return self.nombre


class Profile(models.Model):
    # Definimos constantes para los roles y evitamos repetir strings sueltos
    ROLE_EDITOR = "EDITOR"
    ROLE_CONSULTOR = "CONSULTOR"
    ROLE_ADMIN = "ADMIN"

    # Choices que usamos en formularios y validaciones
    ROLE_CHOICES = [
        (ROLE_EDITOR, "Editor"),
        (ROLE_CONSULTOR, "Consultor"),
        (ROLE_ADMIN, "Admin"),
    ]

    # Relación 1–1 con el usuario (usar AUTH_USER_MODEL = a prueba de futuro)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,      # si borramos el usuario, borramos también su perfil
        related_name="profile",        # accedemos como user.profile
    )

    # Guardamos el rol; por defecto, todo usuario nuevo será "Consultor"
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_CONSULTOR,
    )

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    # Mostramos nombre completo si está definido; de lo contrario, el username
    def __str__(self) -> str:
        # Muestra nombre completo si existe; si no, username
        nombre = getattr(self.user, "get_full_name", lambda: "")() or self.user.username
        return f"{nombre} ({self.role})"


    # Helpers: nos permiten consultar de forma más legible el rol del usuario  
    @property
    def is_admin(self) -> bool:
        return self.role == self.ROLE_ADMIN

    @property
    def is_editor(self) -> bool:
        return self.role == self.ROLE_EDITOR

    @property
    def is_consultor(self) -> bool:
        return self.role == self.ROLE_CONSULTOR


class UsuarioEditorial(models.Model):
    # Relación M:N entre usuario y editorial (tabla puente)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)

    class Meta:
        # Aseguramos que no se repita la combinación usuario-editorial
        constraints = [
            models.UniqueConstraint(
                fields=["user", "editorial"],
                name="unique_usuario_editorial",
            )
        ]
        verbose_name = "Usuario de editorial"
        verbose_name_plural = "Usuarios de editorial"
    
    # Representamos la relación en formato legible
    def __str__(self) -> str:
        return f"{self.user} ↔ {self.editorial}"
