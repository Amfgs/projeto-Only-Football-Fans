from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('/emocao/')),  # redireciona para a página inicial do app emocao
    path('emocao/', include('emocao.urls')),  # inclui as URLs do app emocao
    path('partidas/', include('partidas.urls')),  # adiciona o app partidas
    path('accounts/', include('usuarios.urls')),  # adiciona o app usuarios
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]

