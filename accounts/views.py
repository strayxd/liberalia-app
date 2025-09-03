# accounts/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .forms import EmailLoginForm  

User = get_user_model()


class LoginView(View):
    template_name = 'accounts/login.html'  
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')  
        return render(request, self.template_name, {'form': EmailLoginForm()})

    def post(self, request):
        form = EmailLoginForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Revisa los campos del formulario.')
            return render(request, self.template_name, {'form': form})

        email = form.cleaned_data['email'].strip().lower()
        password = form.cleaned_data['password']

        try:
            user = User.objects.get(email__iexact=email)
            user_auth = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user_auth = None

        if user_auth is None:
            messages.error(request, 'Correo o contraseña inválidos.')
            return render(request, self.template_name, {'form': form})

        login(request, user_auth)
        messages.success(request, '¡Bienvenido!')
        return redirect('/')


def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada.')
    return redirect('accounts:login')


def home(request):
    if request.user.is_authenticated:
        return HttpResponse("<h2>Hola, %s</h2><p><a href='/accounts/logout/'>Cerrar sesión</a></p>" %
                            request.user.get_username())
    return HttpResponse("<h2>Sistema de Gestión de Novedades Editoriales</h2>" "<p>"
    "<a href='/accounts/login/'>Iniciar sesión</a></p>")
