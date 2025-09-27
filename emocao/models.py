from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class AvaliacaoEstadio(models.Model): # Classe criada; essa vai guardar no banco de dados as informações que o usuário inserir

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Assume uma relação de 1:N, onde um único usuário pode fazer várias avaliações, e todas essas, pertencem a esse único usuário
    estadio = models.CharField(max_length=100, blank=False) # Cria um campo de texto de no máximo 100 caracteres para o usuário inserir o nome do estário que deseja avaliar. 'blank=False' significa que o usuário necessariamente deve preencher esse campo e ele será automaticamente guardado no banco de dados

    avaliacao_experiencia = models.IntegerField( # Define a forma de avaliacao da experiencia do usuário a partida
        choices=[ # Determina as únicas cinco possibilidades de avaliação
            (1, '★☆☆☆☆ - Ruim'),
            (2, '★★☆☆☆ - Fraca'),
            (3, '★★★☆☆ - Média'),
            (4, '★★★★☆ - Boa'),
            (5, '★★★★★ - Incrível'),
        ],
        validators=[MinValueValidator(1), MaxValueValidator(5)], # Define o máximo de estrelas (5) e o mínimo (1)
        blank=False, # Assume como um campo obrigatório
        default = 3
    )

    comentario_estadio = models.TextField(blank=True, null=True) # Cria um espaço de entrada de comentário opcional de avaliação da partida

    data_avaliacao = models.DateTimeField(auto_now_add=True) # Adiciona a data de avaliação feita pelo usuário a esse estádio

    def __str__(self): # Por padrão, mostra o nome do usuário que fez a avaliação e qual foi a sua avaliação
        return f"Usuário: {self.usuario.username} - Avaliação: {self.avaliacao_experiencia}"


# ====== ADICIONADO MODELO MINIMO TIME ======
class Time(models.Model): # Modelo mínimo para Time, necessário para rodar AvaliacaoTorcida
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
# ==========================================


# Define um novo modelo chamado 'AvaliacaoTorcida', que será mapeado para uma tabela no banco de dados.
class AvaliacaoTorcida(models.Model):
    time = models.CharField(max_length=100)
    comentario_torcida = models.TextField(blank=True, null=True)
    emocao = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    presenca = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    data_criacao = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Avaliação de {self.time} - Emoção: {self.emocao}, Presença: {self.presenca}"
