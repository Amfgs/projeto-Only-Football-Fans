from django.shortcuts import render, redirect, get_object_or_404
from .models import Partida
from .forms import PartidaForm, AvaliacaoPartidaForm

# Lista todas as partidas registradas
def lista_partidas(request):
    partidas = Partida.objects.all().order_by('-data')
    return render(request, 'partidas/lista_partidas.html', {'partidas': partidas})

# Registrar nova partida
def registrar_partida(request):
    if request.method == 'POST':
        form = PartidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('partidas:lista_partidas')
    else:
        form = PartidaForm()
    return render(request, 'partidas/registrar_partida.html', {'form': form})

# Avaliar partida (pop-up)
def avaliar_partida(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)
    if request.method == 'POST':
        form = AvaliacaoPartidaForm(request.POST, instance=partida)
        if form.is_valid():
            form.save()
            return redirect('partidas:lista_partidas')
    else:
        form = AvaliacaoPartidaForm(instance=partida)
    return render(request, 'partidas/avaliar_partida.html', {'form': form, 'partida': partida})
