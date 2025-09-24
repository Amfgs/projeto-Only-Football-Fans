from django.shortcuts import render
from .models import HistoricoPartida

def listar_historico(request):
    historicos = HistoricoPartida.objects.all().order_by('-data')
    return render(request, 'partidas/lista_historico.html', {'historicos': historicos})

from django.shortcuts import render
from .models import Partida

def lista_partidas(request):
    partidas = Partida.objects.all().order_by('-data')  # Mais recentes primeiro
    return render(request, 'partidas/lista_partidas.html', {'partidas': partidas})
