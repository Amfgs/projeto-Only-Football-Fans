from django.urls import path
from . import views

app_name = 'partidas'

urlpatterns = [
    path('historico/', views.listar_historico, name='listar_historico'),
]
