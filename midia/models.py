from django.db import models
from django.utils import timezone

class Definicao(models.Model):
    jogo = models.CharField(max_length=200)  # referência do jogo
    descricao = models.CharField(max_length=500, blank=True)  # descrição opcional
    criado_em = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.jogo} - {self.descricao or 'Sem descrição'}"


class Imagem(models.Model):
    definicao = models.ForeignKey(
        Definicao,
        on_delete=models.CASCADE,
        related_name="imagens"
    )
    arquivo = models.ImageField(upload_to="imagens/")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagem da partida {self.definicao.id}"


class Video(models.Model):
    definicao = models.ForeignKey(
        Definicao,
        on_delete=models.CASCADE,
        related_name="videos"
    )
    arquivo = models.FileField(upload_to="videos/")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vídeo da partida {self.definicao.id}"


class Audio(models.Model):
    definicao = models.ForeignKey(
        Definicao,
        on_delete=models.CASCADE,
        related_name="audios"
    )
    arquivo = models.FileField(upload_to="audios/")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Áudio da partida {self.definicao.id}"
