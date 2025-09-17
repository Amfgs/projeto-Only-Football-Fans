from django.db import models
from django.utils import timezone
# Create your models here.

class Definicao(models.Model):
    jogo = models.CharField(max_length=200) #Depois mudarei para ser somente a referência do jogo ja colocado no app de partida
    descricao = models.CharField(blank=True) #Pode ser a descricao da partida tambem vindo do app de partida ou so a descricao da midia ou ambas marcam
    criado_em = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.jogo} - {self.descricao}"
    
class Imagem(models.Model):
    definicao = models.ForeignKey(Definicao, on_delete=models.CASCADE, related_name="Imagens")
    arquivo = models.ImageField(upload_to="Imagens/")
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Imagem da partida {self.definicao.id}"
    
class Video(models.Model):
    definicao = models.ForeignKey(Definicao, on_delete=models.CASCADE, related_name="videos")
    arquivo = models.FileField(upload_to="videos/")
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Vídeo da partida {self.definicao.id}"


class Audio(models.Model):
    definicao = models.ForeignKey(Definicao, on_delete=models.CASCADE, related_name="audios")
    arquivo = models.FileField(upload_to="audios/")
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Áudio da partida {self.definicao.id}"