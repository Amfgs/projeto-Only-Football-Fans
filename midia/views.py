from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Imagem, Video, Audio, Definicao
from partidas.models import Partida

# Create your views here.

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

        return redirect('midia:galeria')

    return render(request, 'midia/adicionar_midia.html', {
        'partida': partida,
        'definicao': definicao
    })

