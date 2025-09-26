# partidas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Partida, Gol, AvaliacaoPartida, Time
from django.contrib.auth.decorators import login_required
from django.db import transaction

def lista_partidas(request):
    """
    Lista as partidas disponíveis para avaliação.
    Observação: As partidas podem ser criadas pelo app do registrador.
    """
    partidas = Partida.objects.all().order_by('-data')
    return render(request, 'partidas/lista_partidas.html', {'partidas': partidas})


@login_required  # força login para avaliarem (opcional)

def registrar_partida(request):
    if request.method == 'POST':
        # Pegando dados do POST
        time_casa_id = request.POST.get('time_casa')
        time_visitante_id = request.POST.get('time_visitante')
        data = request.POST.get('data')

        # Criando a partida
        partida = Partida.objects.create(
            time_casa_id=time_casa_id,
            time_visitante_id=time_visitante_id,
            data=data
        )
        return redirect('partidas:lista_partidas')  # redireciona para a lista de partidas

    # GET → renderiza o formulário
    times = Time.objects.all()  # pega todos os times cadastrados
    return render(request, 'partidas/registrar_partida.html', {'times': times})

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