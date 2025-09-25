from django.shortcuts import render, redirect, get_object_or_404
from .models import AvaliacaoTorcida, AvaliacaoEstadio, Time
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django import forms # Importa sistema de formulário do Django
from django.core.paginator import Paginator # Importa sistema de paginação do Django

def index(request):
    return render(request, 'emocao/index.html')  # cria o template index.html dentro de emocao/templates/emocao/

class AvaliacaoEstadioForm(forms.ModelForm): # Cria um modelo de formulário baseado na estrutura do modelo de 'AvaliacaoEstadio'
    class Meta: # Cria uma classe baseada nos Metadados da classe de 'AvaliacaoEstadio'

        model = AvaliacaoEstadio # Define a qual classe o modelo será gerado
        fields = ['estadio', 'avaliacao_experiencia', 'comentario'] # Define os campos que irão compor o formulário

        widgets = {
            'avaliacao_experiencia': forms.RadioSelect(choices=AvaliacaoEstadio._meta.get_field('avaliacao_experiencia').choices), # Botões de rádio no formulário.
            'comentario': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escreva seu comentário...'}), # àrea de texto com três linhas e um imperativo de comando
        }

@login_required # Garante que o usuário esteja logado, caso não, o mesmo será redirecionado para a página de login

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
    
@login_required
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