# partidas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Partida, Gol, AvaliacaoPartida
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

def criar_partida(request):
    if request.method == "POST":
        time_casa = request.POST.get("time_casa")
        time_visitante = request.POST.get("time_visitante")
        adversario = request.POST.get("adversario")
        data = request.POST.get("data")  # virá no formato datetime-local (HTML5)

        # cria a partida no banco
        Partida.objects.create(
            time_casa=time_casa,
            time_visitante=time_visitante,
            adversario=adversario,
            data=data
        )

        return redirect("lista_partidas")  # ajuste para sua rota

    return render(request, "partida_form.html")

def avaliar_partida(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)

    if request.method == "POST":
        nota = request.POST.get("nota")
        melhor_jogador = request.POST.get("melhor_jogador")
        pior_jogador = request.POST.get("pior_jogador")
        comentario = request.POST.get("comentario")

        AvaliacaoPartida.objects.create(
            partida=partida,   # associa a avaliação a essa partida
            nota=nota,
            melhor_jogador=melhor_jogador,
            pior_jogador=pior_jogador,
            comentario=comentario
        )

        return redirect("detalhe_partida", partida_id=partida.id)  # ajuste conforme sua rota

    return render(request, "avaliacao_partida_form.html", {"partida": partida})

def registrar_gols(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)

    if request.method == "POST":
        autores = request.POST.getlist("autor")
        minutos = request.POST.getlist("minuto")

        # cria os gols
        for autor, minuto in zip(autores, minutos):
            if autor and minuto:  # evita criar vazio
                Gol.objects.create(
                    partida=partida,
                    autor=autor,
                    minuto=minuto
                )

        return redirect("detalhe_partida", partida_id=partida.id)

    return render(request, "registrar_gols.html", {"partida": partida})