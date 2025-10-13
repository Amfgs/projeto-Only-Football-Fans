from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

app_name = 'core'

urlpatterns = [
    # Emoções
    path('emocao/', views.home, name='emocao_index'),
    path('emocao/avaliacao/inicio/', views.avaliacao_inicio, name='avaliacao_inicio'),
    path('emocao/avaliar/<int:time_id>/', views.avaliar_time, name='avaliar_time'),
    path('emocao/resultado/', views.resultado_avaliacoes, name='resultado_avaliacoes'),
    path('emocao/nova-avaliacao/', views.nova_avaliacao, name='nova_avaliacao'),
    path('partidas/avaliar_torcida/<int:partida_id>/', views.avaliar_torcida, name='avaliar_torcida'),
    path('partidas/avaliar_torcida/<int:partida_id>/2/', lambda r, partida_id: views.avaliar_torcida(r, partida_id, time_index=2), name='avaliar_torcida_segundo'),


    # Mídia
    path('midia/galeria/', views.galeria, name='galeria'),
    path('midia/adicionar/<int:partida_id>/', views.adicionar_midia, name='adicionar_midia'),

    # Partidas
    path('partidas/', views.lista_partidas, name='lista_partidas'),
    path('partidas/registrar/', views.registrar_partida, name='registrar_partida'),
    path('partidas/avaliar/<int:partida_id>/', views.avaliar_partida, name='avaliar_partida'),

    # Usuários
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:login'), name='logout'),
    path('partidas/ver/<int:partida_id>/', views.ver_avaliacao, name='ver_avaliacao'),

    # Página inicial
    path('', views.home, name='home'),
]
