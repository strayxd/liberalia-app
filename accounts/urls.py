from django.urls import path
from .views import LoginView, logout_view  # usa tus vistas reales

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]