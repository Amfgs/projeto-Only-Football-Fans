from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Q 

from .models import (
    AvaliacaoTorcida, AvaliacaoEstadio, Time, Partida, Imagem, Video, Audio,
    Definicao, Gol, AvaliacaoPartida, Jogador, Link
)

Usuario = get_user_model()

def get_partidas_context(request):
    partidas = Partida.objects.filter(usuario=request.user).order_by("-data")
    avaliacoes = AvaliacaoPartida.objects.filter(usuario=request.user)
    partidas_avaliadas = {a.partida_id for a in avaliacoes}
    return {"partidas": partidas, "partidas_avaliadas": partidas_avaliadas}


# ----------------------------
# USUÁRIOS: login, logout, registro
# ----------------------------


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # >>> ADIÇÃO: ler os campos novos do formulário
        time_favorito = request.POST.get('time_favorito') or ''
        avatar = request.FILES.get('avatar')  # precisa do enctype no form

        if password != confirm_password:
            return render(request, 'usuarios/register.html', {'error': 'Senhas não coincidem'})
        if Usuario.objects.filter(username=username).exists():
            return render(request, 'usuarios/register.html', {'error': 'Usuário já existe'})
        if Usuario.objects.filter(email=email).exists():
            return render(request, 'usuarios/register.html', {'error': 'Email já cadastrado'})

        # >>> ADIÇÃO: salvar já com time_favorito e avatar
        user = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password,
            time_favorito=time_favorito,
            avatar=avatar
        )

        login(request, user)
        return redirect('core:home')

    return render(request, 'usuarios/register.html')

user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)  # Cria sessão persistente
            return redirect('core:home')
        else:
            messages.error(request, "Usuário ou senha incorretos.")

    return render(request, 'usuarios/login.html')


def user_logout(request):
    """Logout do usuário"""
    logout(request)
    return redirect("core:login")


# ----------------------------
# PÁGINA INICIAL
# ----------------------------

def home(request):
    if not request.user.is_authenticated:
        return redirect('core:login')  # redireciona para login
    return render(request, 'base.html')


# ----------------------------
# EMOÇÕES
# ----------------------------

def avaliar_torcida(request, partida_id, time_index=1):
    partida = get_object_or_404(Partida, id=partida_id)
    time = partida.time_casa if time_index == 1 else partida.time_visitante

    if request.method == 'POST':
        AvaliacaoTorcida.objects.create(
            time=request.POST.get('time'),
            comentario_torcida=request.POST.get('comentario'),
            emocao=request.POST.get('emocao'),
            presenca=request.POST.get('presenca')
        )

        # Se avaliou o time 1, redireciona para avaliar o time 2
        if time_index == 1:
            return redirect('core:avaliar_torcida_segundo', partida_id=partida_id)
        else:
            return redirect('core:lista_partidas')

    context = {'time': time, 'partida': partida}
    context.update(get_partidas_context(request))
    return render(request, 'emocao/avaliar_torcida.html', context)



def avaliacao_inicio(request):
    context = {}
    context.update(get_partidas_context(request))
    return render(request, 'emocao/avaliacao_inicio.html', context)

def nova_avaliacao(request):
    if request.method == "POST":
        estadio_nome = request.POST.get("estadio")
        avaliacao_raw = request.POST.get("avaliacao")
        comentario = request.POST.get("comentario")

    # Validação mínima
        if not estadio_nome or not avaliacao_raw:
            return render(request, "emocao/nova_avaliacao.html", {
                "erro": "Preencha todos os campos obrigatórios."
            })

        try:
            avaliacao = int(avaliacao_raw)
        except ValueError:
            return render(request, "emocao/nova_avaliacao.html", {
                "erro": "A avaliação deve ser um número entre 1 e 5."
            })

        # Só associa o usuário se estiver logado
        usuario = request.user if request.user.is_authenticated else None

        AvaliacaoEstadio.objects.create(
            estadio=estadio_nome,
            avaliacao_experiencia=avaliacao,
            comentario_estadio=comentario,
            usuario=usuario
        )

        return render(request, "emocao/avaliacao_sucesso.html")

    context = {}
    context.update(get_partidas_context(request))
    return render(request, "emocao/nova_avaliacao.html", context)



def avaliacoes_anteriores(request):
    page_number = request.GET.get('page', 1)
    avaliacoes = AvaliacaoEstadio.objects.filter(usuario=request.user).order_by('-data_avaliacao')
    paginator = Paginator(avaliacoes, 1)
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    context.update(get_partidas_context(request))
    return render(request, "emocao/avaliacoes_anteriores.html", context)


# Avaliações de torcida (POST direto, sem form)
def avaliar_time(request, time_id):
    time = get_object_or_404(Time, id=time_id)

    if request.method == "POST":
        comentario = request.POST.get("comentario")
        emocao = request.POST.get("emocao")
        presenca = request.POST.get("presenca")

        AvaliacaoTorcida.objects.create(
            comentario=comentario,
            emocao=emocao,
            presenca=presenca,
            time=time
        )

        # Se houver sequência de times a avaliar, redireciona para o próximo
        proximo_time = Time.objects.filter(nome="Time 2").first()
        if proximo_time and time.nome == "Time 1":
            return redirect("avaliar_time", time_id=proximo_time.id)

        return redirect("resultado_avaliacoes")

    context = {"time": time}
    context.update(get_partidas_context(request))
    return render(request, "avaliacao_form.html", context)


def resultado_avaliacoes(request):
    avaliacoes = AvaliacaoTorcida.objects.all()
    context = {"avaliacoes": avaliacoes}
    context.update(get_partidas_context(request))
    return render(request, "emocao/resultado.html", context)


# ----------------------------
# MÍDIA
# ----------------------------

def galeria(request):
    context = {
        "partidas": Partida.objects.filter(usuario=request.user).order_by("-data"),
        "definicoes": Definicao.objects.filter(usuario=request.user)
    }
    context.update(get_partidas_context(request))  # <- adiciona os dados do popup
    return render(request, "midia/galeria.html", context)



def adicionar_midia(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)
    definicao, _ = Definicao.objects.get_or_create(
    jogo=str(partida),
    usuario=request.user,   # garante que cada usuário tem seu próprio conjunto
    defaults={"descricao": ""}
    )

    if request.method == "POST":
        if "imagem" in request.FILES:
            Imagem.objects.create(definicao=definicao, arquivo=request.FILES["imagem"])
        if "video" in request.FILES:
            Video.objects.create(definicao=definicao, arquivo=request.FILES["video"])
        if "audio" in request.FILES:
            Audio.objects.create(definicao=definicao, arquivo=request.FILES["audio"])
        return redirect("core:galeria")

    context = {"partida": partida, "definicao": definicao}
    context.update(get_partidas_context(request))
    return render(request, "midia/adicionar_midia.html", context)


@login_required
def adicionar_link(request, definicao_id):
    """
    View para adicionar um novo link (URL) a uma definição de mídia existente,
    sem usar forms.py, processando o POST diretamente.
    """
    definicao = get_object_or_404(Definicao, pk=definicao_id, usuario=request.user)

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        url = request.POST.get('url')

        if titulo and url:
            Link.objects.create(
                definicao=definicao,
                titulo=titulo,
                url=url
            )
            messages.success(request, f"Link '{titulo}' adicionado com sucesso!")
            return redirect('core:adicionar_midia', partida_id=definicao.id) 
        else:
            messages.error(request, "Título e URL são obrigatórios para adicionar o link.")

    context = {
        'definicao': definicao,
        'page_title': f'Adicionar Link à Partida {definicao.jogo}',
    }
    context.update(get_partidas_context(request))
    return render(request, 'midia/adicionar_link.html', context)

@login_required
def adicionar_link_page(request):
    """
    Lida com o formulário de cadastro de um novo Link.
    """
    if request.method == 'POST':
        nome_do_jogo = request.POST.get('nome_do_jogo')
        url = request.POST.get('url')

        if nome_do_jogo and url:
            #  Como o link não está associado a uma Definicao,
            # ele fica solto (definicao=None)
            Link.objects.create(
                nome_do_jogo=nome_do_jogo,
                url=url,
            )
            messages.success(request, f"Link de {nome_do_jogo} cadastrado com sucesso!")
            # Retorna para a página de lista
            return redirect('core:lista_links') 
        else:
            messages.error(request, "Nome do Jogo e URL são obrigatórios.")

    context = {
        'page_title': 'Cadastrar Novo Link de Jogo',
    }
    context.update(get_partidas_context(request))
    # Renderiza o novo template de formulário
    return render(request, 'midia/adicionar_link_page.html', context)


@login_required
def lista_links(request):
    """
    Lista todos os links de mídia cadastrados pelo usuário.
    """
    from django.db.models import Q 
    
    user_definicoes = Definicao.objects.filter(usuario=request.user)
    
    # Busca links que pertencem a Definições do usuário OU que são soltos (novos)
    links = Link.objects.filter(
        Q(definicao__in=user_definicoes) | Q(definicao__isnull=True)
    ).order_by('-criado_em')

    context = {
        'links': links,
        'page_title': 'Links de Replay e Mídia',
    }
    context.update(get_partidas_context(request))
    # Renderiza o template de listagem 
    return render(request, 'midia/lista_links.html', context)


# ----------------------------
# PARTIDAS
# ----------------------------

def lista_partidas(request):
    partidas = Partida.objects.filter(usuario=request.user).order_by("-data")
    avaliacoes = AvaliacaoPartida.objects.filter(usuario=request.user)
    partidas_avaliadas = {a.partida_id for a in avaliacoes}
    return render(request, "partidas/lista_partidas.html", {"partidas": partidas, "partidas_avaliadas": partidas_avaliadas})



def registrar_partida(request):
    times = Time.objects.all()

    if request.method == "POST":
        time_casa_nome = request.POST.get("time_casa")
        time_visitante_nome = request.POST.get("time_visitante")
        data = request.POST.get("data")

        if request.user.is_authenticated:
            Partida.objects.create(
                usuario=request.user, 
                time_casa=time_casa_nome,
                time_visitante=time_visitante_nome,
                data=data
            )

        return redirect("core:lista_partidas")

    context = {"times": times}
    context.update(get_partidas_context(request))

    return render(request, "partidas/registrar_partida.html", context)


def avaliar_partida(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)

    # ======== ADIÇÃO PARA MENSAGEM DE PARTIDA JÁ AVALIADA ========
    if request.user.is_authenticated:
        ja_avaliou = AvaliacaoPartida.objects.filter(partida=partida, usuario=request.user).exists()
        if ja_avaliou:
            messages.warning(request, "Você já avaliou esta partida!")
            return redirect("core:lista_partidas")
    # ===============================================================

    if request.method == "POST":
        nota = int(request.POST.get("nota", 0))
        melhor_nome = request.POST.get("melhor_jogador", "").strip()
        pior_nome = request.POST.get("pior_jogador", "").strip()
        comentario = request.POST.get("comentario", "")

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

        messages.success(request, "Avaliação registrada com sucesso!")
        return redirect("core:lista_partidas")

    context = {"partida": partida}
    context.update(get_partidas_context(request))
    return render(request, "partidas/avaliar_partida.html", context)

def ver_avaliacao(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)
    avaliacao = AvaliacaoPartida.objects.filter(partida=partida, usuario=request.user).first()

    if not avaliacao:
        messages.error(request, "Você ainda não avaliou esta partida.")
        return redirect("core:lista_partidas")

    context = {"avaliacao": avaliacao, "partida": partida}
    context.update(get_partidas_context(request))
    return render(request, "partidas/ver_avaliacao.html", context)


def registrar_gols(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)

    if request.method == "POST":
        autores = request.POST.getlist("autor")
        minutos = request.POST.getlist("minuto")

        for autor, minuto in zip(autores, minutos):
            if autor and minuto:
                Gol.objects.create(partida=partida, autor=autor, minuto=minuto)

        return redirect("detalhe_partida", partida_id=partida.id)

    context = {"partida": partida}
    context.update(get_partidas_context(request))
    return render(request, "registrar_gols.html", context)
