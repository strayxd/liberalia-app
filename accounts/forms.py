
from django import forms


# Creamos un formulario de login basado en email y contraseña
class EmailLoginForm(forms.Form):
    # Campo de email con validación automática de Django
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',  # usamos estilo Bootstrap
            'placeholder': 'Correo', # texto de ayuda en el input
            'required': 'required', # obligamos a completar el campo
            'autocomplete': 'email' # sugerencia de navegador
        })
    )

     # Campo de contraseña con input oculto (PasswordInput)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', # estilo Bootstrap
            'placeholder': 'Contraseña', # texto de ayuda
            'required': 'required',  # campo obligatorio
            'autocomplete': 'current-password', # sugerencia de navegador
            'minlength': '6' # longitud mínima en frontend
        })
    )
