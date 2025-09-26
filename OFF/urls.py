from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from usuarios import views as usuarios_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login
    path('login/', auth_views.LoginView.as_view(
        template_name='usuarios/login.html'
    ), name='login'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Página inicial (home) após login
    path('', usuarios_views.home, name='home'),

    # Apps
    path('emocao/', include('emocao.urls')),
    path('partidas/', include('partidas.urls')),
    path('accounts/', include('usuarios.urls')),  # se tiver URLs extras do app usuarios
]