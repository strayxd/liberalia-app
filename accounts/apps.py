from django.apps import AppConfig

# Definimos la configuración de la aplicación "accounts"
class AccountsConfig(AppConfig):
    # Indicamos que las claves primarias por defecto serán BigAutoField
    default_auto_field = 'django.db.models.BigAutoField'
    # Especificamos el nombre de la app (usada por Django para reconocerla)
    name = 'accounts'
