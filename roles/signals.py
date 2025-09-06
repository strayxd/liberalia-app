# -------------------------------------------------------------------------------
# Señales para garantizar que cada usuario tenga un Profile asociado.
# Al crear un usuario nuevo, se crea automáticamente su Profile con el rol por defecto.
# También asegura que usuarios existentes sin Profile reciban uno.
# Se usa settings.AUTH_USER_MODEL para no depender del User por defecto.
# -------------------------------------------------------------------------------

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_profile(sender, instance, created, **kwargs):
    """
    - Si el usuario es nuevo: crea su Profile con el rol por defecto (definido en el modelo).
    - Si el usuario ya existía: garantiza que tenga Profile (útil para usuarios antiguos).
    """
    if created:
        # Usuario recién creado → creo el Profile
        Profile.objects.get_or_create(user=instance)
        
    else:
        # Usuario existente: si por alguna razón no tiene Profile, lo creo
        # (esto cubre usuarios viejos creados antes de tener esta señal)
        if not hasattr(instance, "profile"):
            Profile.objects.create(user=instance)




