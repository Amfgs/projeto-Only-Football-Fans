# partidas/urls.py
from django.urls import path
from . import views

app_name = 'partidas'

urlpatterns = [
    path('', views.lista_partidas, name='lista_partidas'),
    # Registrar: se o registrador criar outro app, esta rota pode ser removida
    path('registrar/', views.registrar_partida, name='registrar_partida'),
    # Avaliar: rota principal da sua parte
    path('avaliar/<int:partida_id>/', views.avaliar_partida, name='avaliar_partida'),
]
