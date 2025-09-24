from django.db import models
from django.utils import timezone
from partidas.models import HistoricoPartida

# Create your models here.

class Definicao(models.Model):
    jogo = models.ForeignKey(HistoricoPartida, on_delete=models.CASCADE, related_name="midias")
    descricao = models.CharField(max_length=200, blank=True)  # Pode ser descrição da midia ou da partida
    criado_em = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.jogo} - {self.descricao}"

    
class Imagem(models.Model):
    definicao = models.ForeignKey(Definicao, on_delete=models.CASCADE, related_name="imagens")
    arquivo = models.ImageField(upload_to="imagens/")
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Imagem da partida {self.definicao.jogo.id}"

class Video(models.Model):
    definicao = models.ForeignKey(Definicao, on_delete=models.CASCADE, related_name="videos")
    arquivo = models.FileField(upload_to="videos/")
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Vídeo da partida {self.definicao.jogo.id}"

class Audio(models.Model):
    definicao = models.ForeignKey(Definicao, on_delete=models.CASCADE, related_name="audios")
    arquivo = models.FileField(upload_to="audios/")
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Áudio da partida {self.definicao.jogo.id}"
