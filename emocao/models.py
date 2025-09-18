from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class AvaliacaoEstadio(models.Model): # Classe criada; essa vai guardar no banco de dados as informações que o usuário inserir

    usuario = models.ForeignKey(User, on_delete=models.CASCADE) # Assume uma relação de 1:N, onde um único usuário pode fazer várias avaliações, e todas essas, pertecem a esse único usuário
    estadio = models.CharField(max_length=100, blank=False) # Cria um campo de texto de no máximo 100 caracteres para o usuário inserir o nome do estário que deseja avaliar. 'blank=False' significa que o usuário necessariamente deve preencher esse campo e ele será automaticamente guradado no banco de dados (entender melhor a diferença entre 'blank' e 'null' no BD)

    avaliacao_experiencia = models.IntegerField( # Define a forma de avaliacao da experiencia do usuário a partida
    choices=[ # Determina as únicas cinco possibilidades de avaliação(o nome deve ser 'choices', isto é um nome conhecido e já interpretado)
        (1, '★☆☆☆☆ - Ruim'),
        (2, '★★☆☆☆ - Fraca'),
        (3, '★★★☆☆ - Média'),
        (4, '★★★★☆ - Boa'),
        (5, '★★★★★ - Incrível'),
    ],
    validators=[MinValueValidator(1), MaxValueValidator(5)], # Define o máximo de estrelas (5) e o mínimo (1)
    blank=False # Assume como um campo obrigatório
)

    comentario = models.TextField(blank=True, null=True) # Cria um espaço de entrada de comentário opcional de avalição da partida, esse que, se não for deixado em branco, será armazenado em branco no BD

    data_avaliacao = models.DateTimeField(auto_now_add=True) # Adiciona a data de avaliação da feita pelo usuário a esse estádio

    def __str__(self): # Por padrão, mostra o nome do usuário que fez a avaliação e qual foi a sua avaliação
        return f"{self.usuario.username} - {self.avaliacao_experiencia})"

# Create your models here.

# Define um novo modelo chamado 'AvaliacaoTorcida', que será mapeado para uma tabela no banco de dados.
class AvaliacaoTorcida(models.Model):
    #    Campo de chave estrangeira (ForeignKey) para relacionar a avaliação a um 'Time'.
    #    "emocoes.Time": Evita importação circular, referenciando o modelo como uma string 'app.Model'.
    #    on_delete=models.CASCADE: Garante que, se um time for deletado, todas as suas avaliações também serão.
    #    related_name="avaliacoes": Permite acessar as avaliações de um time facilmente (ex: meu_time.avaliacoes.all()).
    time = models.ForeignKey("emocoes.Time", on_delete=models.CASCADE, related_name="avaliacoes")

    #    Campo de texto para o comentário do torcedor.
    #    blank=True: Permite que o campo seja enviado vazio em um formulário.
    #    null=True: Permite que o valor no banco de dados seja NULL (nenhum valor).
    comentario = models.TextField(blank=True, null=True)

    #    Campo para a nota de 'emoção' (1 a 5).
    #    PositiveSmallIntegerField: Otimizado para números inteiros pequenos e não negativos.
    #    choices=[...]: Cria uma lista de opções [(valor_no_banco, valor_exibido)], validando a entrada.
    emocao = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    #    Campo para a nota de 'presença' (1 a 5), com a mesma lógica do campo 'emocao'.
    presenca = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    #    Campo de data e hora que registra automaticamente o momento da criação do registro.
    #    auto_now_add=True: Preenche o campo com a data/hora atual apenas na primeira vez que o objeto é salvo.
    data_criacao = models.DateTimeField(auto_now_add=True)

    #     Método especial que define a representação em string de um objeto deste modelo.
    #     Útil para visualização no painel de administração do Django, em logs ou no console.
    def __str__(self):
        #     Retorna uma string formatada com informações úteis sobre a avaliação.
        return f"Avaliação de {self.time.nome} - Emoção: {self.emocao}, Presença: {self.presenca}"
