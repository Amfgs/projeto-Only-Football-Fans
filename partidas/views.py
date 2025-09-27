# partidas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Partida, Gol, Time, Jogador
from django.contrib.auth.decorators import login_required
from partidas.models import AvaliacaoPartida

def lista_partidas(request):
    """
    Lista as partidas disponíveis para avaliação.
    Observação: As partidas podem ser criadas pelo app do registrador.
    """
    partidas = Partida.objects.all().order_by('-data')
    return render(request, 'partidas/lista_partidas.html', {'partidas': partidas})

@login_required
def registrar_partida(request):
    times = Time.objects.all()  # pega todos os times cadastrados (para sugestões no template)

    if request.method == 'POST':
        # Recebe o nome digitado pelo usuário
        time_casa_nome = request.POST.get('time_casa')
        time_visitante_nome = request.POST.get('time_visitante')
        data = request.POST.get('data')

        # Cria a partida usando os nomes digitados
        Partida.objects.create(
            time_casa=time_casa_nome,
            time_visitante=time_visitante_nome,
            data=data
        )
        return redirect('partidas:lista_partidas')  # redireciona para a lista de partidas

    # GET → renderiza o formulário
    return render(request, 'partidas/registrar_partida.html', {'times': times})

@login_required
def avaliar_partida(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)

    if request.method == "POST":
        nota = int(request.POST.get('nota', 0))
        melhor_nome = request.POST.get('melhor_jogador', '').strip()
        pior_nome = request.POST.get('pior_jogador', '').strip()
        comentario = request.POST.get('comentario_avaliacao', '')

        # Cria ou pega os jogadores pelo nome
        melhor_jogador = Jogador.objects.get_or_create(nome=melhor_nome)[0] if melhor_nome else None
        pior_jogador = Jogador.objects.get_or_create(nome=pior_nome)[0] if pior_nome else None

        AvaliacaoPartida.objects.create(
            partida=partida,
            usuario=request.user if request.user.is_authenticated else None,
            nota=nota,
            melhor_jogador=melhor_jogador,
            pior_jogador=pior_jogador,
            comentario_avaliacao=comentario
        )

        return redirect('partidas:lista_partidas')

    return render(request, 'partidas/avaliar_partida.html', {'partida': partida})

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