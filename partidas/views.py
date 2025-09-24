# partidas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Partida
from .forms import PartidaForm, AvaliacaoPartidaForm, GolFormSet
from django.contrib.auth.decorators import login_required
from django.db import transaction

def lista_partidas(request):
    """
    Lista as partidas disponíveis para avaliação.
    Observação: As partidas podem ser criadas pelo app do registrador.
    """
    partidas = Partida.objects.all().order_by('-data')
    return render(request, 'partidas/lista_partidas.html', {'partidas': partidas})


def registrar_partida(request):
    """
    View de registrar partida (placeholder).
    NOTE: Se o outro integrante fizer o app de registro, esta view pode ser removida.
    Aqui está apenas como utilitário para testar localmente.
    """
    if request.method == 'POST':
        form = PartidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('partidas:lista_partidas')
    else:
        form = PartidaForm()
    return render(request, 'partidas/registrar_partida.html', {'form': form})


@login_required  # força login para avaliarem (opcional)
def avaliar_partida(request, partida_id):
    """
    View principal da sua parte: permite avaliar uma partida e opcionalmente
    registrar os autores/minutos dos gols (apenas como dado complementar).
    - Salva uma nova instância de AvaliacaoPartida (não altera Partida)
    - Salva os Gols via GolFormSet vinculados à partida
    """
    partida = get_object_or_404(Partida, id=partida_id)

    # formset para gols (opcional)
    if request.method == 'POST':
        form = AvaliacaoPartidaForm(request.POST)
        formset = GolFormSet(request.POST, instance=partida)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                aval = form.save(commit=False)
                aval.partida = partida
                aval.usuario = request.user
                aval.save()
                formset.save()
            return redirect('partidas:lista_partidas')
    else:
        form = AvaliacaoPartidaForm()
        formset = GolFormSet(instance=partida)

    return render(request, 'partidas/avaliar_partida.html', {
        'form': form,
        'formset': formset,
        'partida': partida
    })