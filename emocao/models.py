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