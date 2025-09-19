from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('/emocao/')),  # redireciona para a página inicial do app emocao
    path('emocao/', include('emocao.urls')),  # inclui as URLs do app emocao
    path('partidas/', include('partidas.urls')),  # adiciona o app partidas
]

