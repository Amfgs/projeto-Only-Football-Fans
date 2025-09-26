from django.urls import path
from . import views

app_name = 'partidas'

urlpatterns = [
    path('lista/', views.lista_partidas, name='lista_partidas'),
    path('registrar/', views.registrar_partida, name='registrar_partida'),
    path('avaliar/<int:partida_id>/', views.avaliar_partida, name='avaliar_partida'),
]
