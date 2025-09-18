from django.shortcuts import render, redirect, get_object_or_404
from .models import AvaliacaoTorcida, Time
from django.http import HttpResponse
from django import forms

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