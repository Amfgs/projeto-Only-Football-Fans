
from django.urls import path

from . import views
# Importa as views de autenticação do Django, dando a elas o apelido 'auth_views'
# Isso evita conflito de nomes com as suas views
from django.contrib.auth import views as auth_views

# Lista de padrões de URL do seu aplicativo
urlpatterns = [
    # Rotas criadas para o cadastro
    path('register/', views.register, name='register'),
    
    # Rota para o login
    path('login/',
         # Usa a view de login padrão do Django, o que economiza tempo de codificação
         auth_views.LoginView.as_view(template_name='usuarios/login.html'),
         name='login'),
]