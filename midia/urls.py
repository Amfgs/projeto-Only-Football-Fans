from django.urls import path
from . import views

app_name = 'midia'

urlpatterns = [
    # Esta é a nova rota principal de "Assistir jogos"
    path("assistir/", views.lista_links_partidas, name="lista_links_partidas"), 
    
    # Rota existente para o formulário de adição (vídeos, imagens, etc.)
    path("adicionar/<int:partida_id>/", views.adicionar_midia, name="adicionar_midia"), 
    
    # Sua rota 'galeria' original
    path("galeria/", views.galeria, name="galeria"), 
]