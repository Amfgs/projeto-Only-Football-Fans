from django.db import models
from django.utils import timezone

# Histórico de partidas
class HistoricoPartida(models.Model):
    usuario = models.CharField(max_length=200)
    time_id = models.IntegerField()
    nota = models.IntegerField()
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario} - Time {self.time_id} - Nota {self.nota}"

# Definição de mídia (referência ao jogo)
class Definicao(models.Model):
    jogo = models.ForeignKey('HistoricoPartida', on_delete=models.CASCADE, related_name="midias")
    descricao = models.CharField(max_length=200, blank=True)
    criado_em = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.jogo} - {self.descricao}"

# Imagens
class Imagem(models.Model):
    definicao = models.ForeignKey('Definicao', on_delete=models.CASCADE, related_name="imagens")
    arquivo = models.ImageField(upload_to="imagens/")
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Imagem da partida {self.definicao.id}"

# Vídeos
class Video(models.Model):
    definicao = models.ForeignKey('Definicao', on_delete=models.CASCADE, related_name="videos")
    arquivo = models.FileField(upload_to="videos/")
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Vídeo da partida {self.definicao.id}"

# Áudios
class Audio(models.Model):
    definicao = models.ForeignKey('Definicao', on_delete=models.CASCADE, related_name="audios")
    arquivo = models.FileField(upload_to="audios/")
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Áudio da partida {self.definicao.id}"
