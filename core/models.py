# core/models.py
from django.db import models
from django.utils import timezone

class HistoricoPartida(models.Model):
    usuario = models.CharField(max_length=200)
    time_id = models.IntegerField()
    nota = models.IntegerField()
    data = models.DateTimeField(default=timezone.now)

class Definicao(models.Model):
    jogo = models.ForeignKey(HistoricoPartida, on_delete=models.CASCADE, related_name="midias")
    descricao = models.CharField(max_length=200, blank=True)
    criado_em = models.DateField(default=timezone.now)

class Imagem(models.Model):
    definicao = models.ForeignKey(Definicao, on_delete=models.CASCADE, related_name="imagens")
    arquivo = models.ImageField(upload_to="imagens/")
    criado_em = models.DateTimeField(default=timezone.now)

# e Video, Audio...
