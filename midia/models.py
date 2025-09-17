from django.db import models
from django.utils import timezone
# Create your models here.

class Definicao(models.Model):
    jogo = models.CharField(max_length=200) #Depois mudarei para ser somente a referência do jogo ja colocado no app de partida
    descricao = models.CharField(blank=True) #Pode ser a descricao da partida tambem vindo do app de partida ou so a descricao da midia ou ambas marcam
    criado_em = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.jogo} - {self.descricao}"
    

