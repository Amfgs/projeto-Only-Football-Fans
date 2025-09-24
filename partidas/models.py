from django.db import models
from django.utils import timezone

# Histórico simples de partidas ou avaliações de partidas
class HistoricoPartida(models.Model):
    usuario = models.CharField(max_length=200)
    time_id = models.IntegerField()
    nota = models.IntegerField()
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario} - Time {self.time_id} - Nota {self.nota}"


# Modelo que representa um jogador de futebol
class Jogador(models.Model):
    nome = models.CharField(max_length=100)  # Nome do jogador
    
    def __str__(self):
        return self.nome  # Exibe o nome do jogador


# Modelo que representa uma partida de futebol com avaliação
class Partida(models.Model):
    adversario = models.CharField(max_length=100)  # Nome do time adversário
    data = models.DateTimeField(default=timezone.now)  # Data e hora da partida
    placar_time = models.IntegerField(default=0)  # Gols do nosso time
    placar_adversario = models.IntegerField(default=0)  # Gols do adversário
    nota = models.IntegerField(default=0)  # Nota da partida (0-5)
    
    # Melhor jogador da partida
    melhor_jogador = models.ForeignKey(
        Jogador,
        on_delete=models.SET_NULL,
        related_name='melhor_em_partidas',
        null=True,
        blank=True
    )
    
    # Pior jogador da partida
    pior_jogador = models.ForeignKey(
        Jogador,
        on_delete=models.SET_NULL,
        related_name='pior_em_partidas',
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f"Partida contra {self.adversario} em {self.data.date()}"


# Modelo que representa gols de uma partida
class Gol(models.Model):
    partida = models.ForeignKey(
        Partida,
        on_delete=models.CASCADE,
        related_name='gols'
    )
    autor = models.ForeignKey(
        Jogador,
        on_delete=models.SET_NULL,
        null=True
    )
    minuto = models.PositiveIntegerField()  # Minuto do gol

    def __str__(self):
        return f"Gol de {self.autor} aos {self.minuto}' na partida {self.partida}"
