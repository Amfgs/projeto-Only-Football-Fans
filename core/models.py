from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # Para vincular usuários

# ========================
# Historico de partidas
# ========================
class HistoricoPartida(models.Model):
    usuario = models.CharField(max_length=200)
    time_id = models.IntegerField()
    nota = models.IntegerField()
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario} - Time {self.time_id} - Nota {self.nota}"

# ========================
# Definição e mídias
# ========================
class Definicao(models.Model):
    jogo = models.ForeignKey('HistoricoPartida', on_delete=models.CASCADE, related_name="midias")
    descricao = models.CharField(max_length=200, blank=True)
    criado_em = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.jogo} - {self.descricao}"

class Imagem(models.Model):
    definicao = models.ForeignKey('Definicao', on_delete=models.CASCADE, related_name="imagens")
    arquivo = models.ImageField(upload_to="imagens/")
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Imagem da partida {self.definicao.jogo.id}"

class Video(models.Model):
    definicao = models.ForeignKey('Definicao', on_delete=models.CASCADE, related_name="videos")
    arquivo = models.FileField(upload_to="videos/")
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Vídeo da partida {self.definicao.jogo.id}"

class Audio(models.Model):
    definicao = models.ForeignKey('Definicao', on_delete=models.CASCADE, related_name="audios")
    arquivo = models.FileField(upload_to="audios/")
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Áudio da partida {self.definicao.jogo.id}"

# ========================
# Emoções
# ========================
class Emocao(models.Model):
    usuario = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50)  # feliz, triste etc.
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario} - {self.tipo}"

# ========================
# Usuários
# ========================
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank=True)
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.nickname}"

# ========================
# Extra images (se houver)
# ========================
class ImageExtra(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    arquivo = models.ImageField(upload_to="extra_images/")
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Imagem extra de {self.usuario.user.username}"
