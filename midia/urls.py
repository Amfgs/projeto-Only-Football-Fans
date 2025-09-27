from django.urls import path
from . import views

app_name = 'midia'

urlpatterns = [
    path('galeria/', views.galeria, name='galeria'),
    path('adicionar/<int:partida_id>/', views.adicionar_midia, name='adicionar_midia'),
]
