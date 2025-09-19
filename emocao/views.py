from django.shortcuts import render, redirect, get_object_or_404
from .models import AvaliacaoTorcida, AvaliacaoEstadio, Time
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django import forms

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

def index(request):
    return HttpResponse("Página de emoções da partida!")

# Create your views here.

class AvaliacaoTorcidaForm(forms.ModelForm):
    #  'Meta' é uma classe interna que configura o formulário.
    class Meta:
        #  Especifica que o formulário está vinculado ao modelo 'AvaliacaoTorcida'.
        model = AvaliacaoTorcida
        #  Define quais campos do modelo devem ser exibidos no formulário.
        #    'time' e 'data_criacao' são omitidos pois serão definidos automaticamente.
        fields = ['comentario', 'emocao', 'presenca']
        #  'widgets' permite customizar a aparência dos campos HTML.
        widgets = {
            #  Transforma o campo 'comentario' em uma área de texto (<textarea>) com um placeholder.
            'comentario': forms.Textarea(attrs={'placeholder': 'Adicione os comentários...'}),
            #  Transforma o campo 'emocao' em botões de rádio (<input type="radio">) com rótulos customizados.
            'emocao': forms.RadioSelect(choices=[(i, f"{i} estrela(s)") for i in range(1, 6)]),
            #  Faz o mesmo para o campo 'presenca'.
            'presenca': forms.RadioSelect(choices=[(i, f"{i} estrela(s)") for i in range(1, 6)]),
        }

#     Define a view 'avaliar_time', que lida com a lógica de avaliação de um time específico.
#     Recebe o objeto 'request' e o 'time_id' capturado da URL.
def avaliar_time(request, time_id):
    #  Busca o objeto 'Time' pelo 'id'; se não existir, retorna a página de erro 404.
    time = get_object_or_404(Time, id=time_id)

    #  Verifica se o método da requisição é POST (ou seja, se o formulário foi enviado).
    if request.method == "POST":
        #  Cria uma instância do formulário com os dados enviados na requisição (request.POST).
        form = AvaliacaoTorcidaForm(request.POST)
        #  Valida os dados do formulário (verifica se os campos obrigatórios estão preenchidos, etc.).
        if form.is_valid():
            #  Cria um objeto 'AvaliacaoTorcida' em memória, sem salvar no banco (commit=False).
            avaliacao = form.save(commit=False)
            #  Associa manualmente o time (buscado via 'time_id') à avaliação.
            avaliacao.time = time
            #  Agora, salva o objeto completo no banco de dados.
            avaliacao.save()

            #  Lógica de redirecionamento: se o time avaliado for o "Time 1"...
            if time.nome == "Time 1":
                #  ...tenta encontrar o "Time 2".
                proximo_time = Time.objects.filter(nome="Time 2").first()
                #  Se o "Time 2" existir...
                if proximo_time:
                    #  ...redireciona o usuário para a página de avaliação do "Time 2".
                    return redirect("avaliar_time", time_id=proximo_time.id)
            #  Se a lógica acima não for atendida, redireciona para a página de resultados.
            return redirect("resultado_avaliacoes")
    #  Se o método não for POST (geralmente é GET, quando o usuário acessa a página pela primeira vez)...
    else:
        #  ...cria uma instância vazia do formulário.
        form = AvaliacaoTorcidaForm()
    #  Renderiza o template HTML, passando o formulário e o objeto 'time' para serem usados na página.
    return render(request, "emocoes/avaliar_time.html", {"form": form, "time": time})

#  Define a view 'resultado_avaliacoes' para exibir todas as avaliações.
def resultado_avaliacoes(request):
    #  Busca todos os objetos 'AvaliacaoTorcida' salvos no banco de dados.
    avaliacoes = AvaliacaoTorcida.objects.all()
    #  Renderiza o template de resultados, passando a lista de avaliações no contexto.
    return render(request, "emocoes/resultado.html", {"avaliacoes": avaliacoes})