from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
# IMPORTANTE: Adicionamos LinkPartida aos imports abaixo
from .models import Imagem, Video, Audio, Definicao, LinkPartida 
from partidas.models import Partida

# Create your views here.

def galeria(request):
    partidas = Partida.objects.all().order_by('-data')
    return render(request, 'midia/galeria.html', {'partidas': partidas})

# Esta view é usada tanto para UPLOAD de arquivos (GET/POST) quanto para POST de links
def adicionar_midia(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)

    # Cria ou obtém uma Definicao (Necessário para os modelos Imagem/Video/Audio)
    definicao, created = Definicao.objects.get_or_create(
        jogo=str(partida),
        defaults={'descricao': ''}
    )

    if request.method == "POST":
        
        # LÓGICA EXISTENTE: UPLOAD DE ARQUIVOS (Imagem, Vídeo, Áudio)
        if 'imagem' in request.FILES:
            Imagem.objects.create(definicao=definicao, arquivo=request.FILES['imagem'])

        if 'video' in request.FILES:
            Video.objects.create(definicao=definicao, arquivo=request.FILES['video'])

        if 'audio' in request.FILES:
            Audio.objects.create(definicao=definicao, arquivo=request.FILES['audio'])

        # LÓGICA PARA NOVO LINK (Assistir Jogos)
        if 'link_jogo' in request.POST and request.POST.get('link_jogo'):
            link_url = request.POST.get('link_jogo')
            
            # Pega o nome do usuário logado (ou 'Anônimo')
            if request.user.is_authenticated:
                usuario_logado = request.user.username
            else:
                usuario_logado = 'Anônimo'
                
            # Cria o objeto LinkPartida
            LinkPartida.objects.create(
                partida=partida,
                url_link=link_url,
                usuario=usuario_logado
            )
            
        # Redireciona para a nova lista de links principal
        return redirect('midia:lista_links_partidas')

    # Lógica para GET (se acessada diretamente, mantém a view original para upload)
    return render(request, 'midia/adicionar_midia.html', {
        'partida': partida,
        'definicao': definicao
    })
    
# -----------------------
# NOVA VIEW PRINCIPAL: Lista de Partidas com Links
# -----------------------
def lista_links_partidas(request):
    """Exibe todas as partidas e os links de vídeo associados."""
    
    # Busca todas as partidas
    todas_partidas = Partida.objects.all().order_by('-data') 

    contexto = {
        'partidas': todas_partidas
    }
    
    return render(request, 'midia/lista_links_partidas.html', contexto)