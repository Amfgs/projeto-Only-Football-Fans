from django.db import models
from django.utils import timezone

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
        return self.nome  # Retorna o nome do jogador para facilitar a identificação

# Modelo que representa uma partida de futebol avaliada
class Partida(models.Model):
    adversario = models.CharField(max_length=100)  # Nome do time adversário
    data = models.DateTimeField(default=timezone.now)  # Data e hora da partida (padrão: agora)
    
    placar_time = models.IntegerField(default=0)  # Quantidade de gols do nosso time
    placar_adversario = models.IntegerField(default=0)  # Quantidade de gols do time adversário
    
    nota = models.IntegerField(default=0)  # Nota da partida (de 0 a 5 estrelas)
    
    # Jogador escolhido como craque (melhor jogador) da partida
    melhor_jogador = models.ForeignKey(
        Jogador,  # Relaciona com o jogador
        on_delete=models.SET_NULL,  # Se o jogador for apagado, deixa esse campo vazio (NULL)
        related_name='melhor_em_partidas',  # Nome para acessar as partidas onde o jogador foi o melhor
        null=True,  # Permite valor nulo
        blank=True  # Permite campo em branco no formulário
    )
    
    # Jogador considerado o pior jogador da partida
    pior_jogador = models.ForeignKey(
        Jogador,
        on_delete=models.SET_NULL,
        related_name='pior_em_partidas',  # Nome para acessar partidas onde ele foi o pior
        null=True,
        blank=True
    )
    
    def __str__(self):
        # Retorna uma descrição simples da partida com adversário e data
        return f"Partida contra {self.adversario} em {self.data.date()}"

# Modelo que representa um gol marcado em uma partida
class Gol(models.Model):
    partida = models.ForeignKey(
        Partida,  # Relaciona o gol à partida correspondente
        on_delete=models.CASCADE,  # Se a partida for apagada, apaga os gols relacionados
        related_name='gols'  # Facilita acessar os gols de uma partida (ex: partida.gols.all())
    )
    
    autor = models.ForeignKey(
        Jogador,  # Jogador que marcou o gol
        on_delete=models.SET_NULL,  # Se o jogador for apagado, deixa campo nulo
        null=True
    )
    
    minuto = models.PositiveIntegerField()  # Minuto da partida em que o gol foi marcado (ex: 45, 90)
    
    def __str__(self):
        # Exibe informações sobre o gol: autor, minuto e partida
        return f"Gol de {self.autor} aos {self.minuto}' na partida {self.partida}"
