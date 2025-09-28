from django.shortcuts import render, redirect, get_object_or_404
from .models import AvaliacaoTorcida, AvaliacaoEstadio, Time, Partida, Imagem, Video, Audio, Definicao, Gol, AvaliacaoPartida, Jogador
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django import forms
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, get_user_model, logout, authenticate

@login_required
# Create your views here.
#Início de emocao
def nova_avaliacao(request):
    if request.method == "POST":
        # Pega os valores enviados pelo formulário
        estadio_nome = request.POST.get("estadio")
        avaliacao = request.POST.get("avaliacao")
        comentario = request.POST.get("comentario")

        # Cria a avaliação no banco
        AvaliacaoEstadio.objects.create(
            estadio=estadio_nome,           # se campo CharField
            avaliacao_experiencia=avaliacao,
            comentario_estadio=comentario
        )

        # Redireciona para alguma página, ex: página inicial
        return redirect("core:home")

    # Se for GET, apenas renderiza o template
    return render(request, "core/nova_avaliacao.html")

def nova_avaliacao(request): # Define a requisição da página por uma nova atualização

    if request.method == 'POST': # Garante que o método de acesso do usuário foi no método de requisição, ou seja, o mesmo preencheu e enviou o formulário de nova avaliação, caso fosse 'GET', o mesmo teria apenas entrado no formulário sem enviar sua experiência

        form = AvaliacaoEstadioForm(request.POST) # Cria o formulário com as informções enviadas pelo usuário

        if form.is_valid: # Faz uma validação se todas as entradas do usuário estão em conformidade com os campos de entrada do formulário

            avaliacao = form.save(commit=False) # Cria uma variável de avaliação que credencia o formulário, porém, sem salvá-lo 
            avaliacao.usuario = request.user # Associa o formulário de avaliação credenciado ao respectivo usuário
            avaliacao.save() # Agora sim, com a correta associação, salva no banco de dados
            return render(request, 'emocao/avaliacao_sucesso.html') # Renderiza um HTML de sucesso na nova avaliação
        
    else: # Associa uma requisição ao formulário, sem entrada de dados usando o método 'GET'
        form = AvaliacaoEstadioForm() # Carrega o formulário de avaliação de estádio
        return render(request, 'emocao/nova_avaliacao.html', {'form': form}) # Renderiza a página de nova avaliação
    
def avaliacoes_carrossel(request):
    # Número da página atual (via GET), padrão é 1
    page_number = request.GET.get('page', 1)

    # Filtra as avaliações do usuário logado, da mais recente para a mais antiga
    avaliacoes = AvaliacaoEstadio.objects.filter(usuario=request.user).order_by('-data_avaliacao')

    paginator = Paginator(avaliacoes, 1) # Uma avaliação por página

    # Página atual
    page_obj = paginator.get_page(page_number)

    # Renderiza a página com o objeto de paginação
    return render(request, 'emocao/avaliacoes_carrossel.html', {'page_obj': page_obj}) # Recurso do Django para renderização

def index(request):
    return HttpResponse("Página de emoções da partida!")

# Create your views here.

#-----------------------------------------------------
def criar_avaliacao(request):
    if request.method == "POST":
        comentario = request.POST.get("comentario")
        emocao = request.POST.get("emocao")
        presenca = request.POST.get("presenca")

        # cria e salva o objeto no banco
        AvaliacaoTorcida.objects.create(              #Mudança de forms para POST em avaliar_torcida    
            comentario=comentario,
            emocao=emocao,
            presenca=presenca
        )
        return redirect("lista_avaliacoes")  # ajuste para sua rota

    return render(request, "avaliacao_form.html")
# ----------------------------------------------------

def avaliar_time(request, time_id):
    # Busca o time pelo ID
    time = get_object_or_404(Time, id=time_id)

    if request.method == "POST":
        comentario = request.POST.get("comentario")
        emocao = request.POST.get("emocao")
        presenca = request.POST.get("presenca")

        # Cria e salva a avaliação manualmente
        AvaliacaoTorcida.objects.create(
            comentario=comentario,
            emocao=emocao,
            presenca=presenca,
            time=time  # associa o time à avaliação
        )

        # Se for o Time 1, redireciona para avaliar o Time 2
        if time.nome == "Time 1":
            proximo_time = Time.objects.filter(nome="Time 2").first()
            if proximo_time:
                return redirect("avaliar_time", time_id=proximo_time.id)

        # Caso contrário, vai direto para os resultados
        return redirect("resultado_avaliacoes")

    # Renderiza o template do formulário manual
    return render(request, "avaliacao_form.html", {"time": time})

#  Define a view 'resultado_avaliacoes' para exibir todas as avaliações.
def resultado_avaliacoes(request):
    #  Busca todos os objetos 'AvaliacaoTorcida' salvos no banco de dados.
    avaliacoes = AvaliacaoTorcida.objects.all()
    #  Renderiza o template de resultados, passando a lista de avaliações no contexto.
    return render(request, "emocoes/resultado.html", {"avaliacoes": avaliacoes})
# Fim de emocao

# Início de midia

def galeria(request):
    partidas = Partida.objects.all().order_by('-data')  # ou qualquer ordenação desejada
    return render(request, 'midia/galeria.html', {'partidas': partidas})

def adicionar_midia(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)

    # Criar ou obter uma Definicao com base no texto da Partida
    definicao, created = Definicao.objects.get_or_create(
        jogo=str(partida),  # usa o __str__ da Partida como chave
        defaults={'descricao': ''}  # descrição vazia por padrão
    )

    if request.method == "POST":
        if 'imagem' in request.FILES:
            Imagem.objects.create(definicao=definicao, arquivo=request.FILES['imagem'])

        if 'video' in request.FILES:
            Video.objects.create(definicao=definicao, arquivo=request.FILES['video'])

        if 'audio' in request.FILES:
            Audio.objects.create(definicao=definicao, arquivo=request.FILES['audio'])

        return redirect('core:galeria')

    return render(request, 'midia/adicionar_midia.html', {
        'partida': partida,
        'definicao': definicao
    })

# Fim de midia

# Início de partidas

def lista_partidas(request):
    """
    Lista as partidas disponíveis para avaliação.
    Observação: As partidas podem ser criadas pelo app do registrador.
    """
    partidas = Partida.objects.all().order_by('-data')
    return render(request, 'partidas/lista_partidas.html', {'partidas': partidas})

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
        return redirect('core:lista_partidas')  # redireciona para a lista de partidas

    # GET → renderiza o formulário
    return render(request, 'partidas/registrar_partida.html', {'times': times})

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

        return redirect('core:lista_partidas')

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

# Fim de partidas

# Início de usuarios

User = get_user_model() 
  # garante que só usuários logados acessam
def home(request):
    return render(request, 'base.html')

def register(request):
    """
    Função que lida com o cadastro de novos usuários sem usar forms.
    """
    if request.method == 'POST':
        # Pega os dados diretamente do POST
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        # Valida campos obrigatórios
        if not username or not email or not password or not password2:
            messages.error(request, "Todos os campos são obrigatórios.")
        elif password != password2:
            messages.error(request, "As senhas não coincidem.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Este nome de usuário já existe.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Este email já está cadastrado.")
        else:
            # Cria o usuário
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            # Loga o usuário automaticamente
            login(request, user)
            return redirect('home')  # Redireciona para a página inicial

    # Se não for POST ou houver erro, renderiza o template
    return render(request, 'usuarios/register.html')


def user_login(request):
    """
    Login de usuários sem usar forms.
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuário ou senha incorretos.")

    return render(request, 'usuarios/login.html')


def user_logout(request):
    """
    Logout do usuário.
    """
    logout(request)
    return redirect('login')

# Fim de usuarios