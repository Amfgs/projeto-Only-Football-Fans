from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

def home(request):
    return redirect('login')

urlpatterns = [
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(
        template_name='usuarios/login.html'  # <-- apontando para o template do app usuarios
    ), name='login'),
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('/emocao/')),  # redireciona para a página inicial do app emocao
    path('emocao/', include('emocao.urls')),  # inclui as URLs do app emocao
    path('partidas/', include('partidas.urls')),  # adiciona o app partidas
    path('accounts/', include('usuarios.urls')),  # adiciona o app usuarios
]

