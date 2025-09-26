from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

# -----------------------
# Modelo do outro integrante
# -----------------------
class HistoricoPartida(models.Model):
    usuario = models.CharField(max_length=200)
    time_id = models.IntegerField()
    nota = models.IntegerField()
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario} - Time {self.time_id} - Nota {self.nota}"

# -----------------------
# Modelo: Time (placeholder)
# -----------------------
class Time(models.Model):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return str(self.nome) if self.nome else "Time sem nome"

# -----------------------
# Modelo: Jogador
# -----------------------
class Jogador(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return str(self.nome) if self.nome else "Jogador sem nome"

# -----------------------
# Modelo: Partida
# -----------------------
class Partida(models.Model):
    time_casa = models.CharField(max_length=100, blank=True, null=True, help_text="Nome do time da casa")
    time_visitante = models.CharField(max_length=100, blank=True, null=True, help_text="Nome do time visitante")
    adversario = models.CharField(max_length=100, blank=True, help_text="Nome do adversário (opcional)")
    data = models.DateTimeField(default=timezone.now)
    registro_externo_id = models.IntegerField(null=True, blank=True, help_text="ID do registro oficial da partida")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        casa = self.time_casa if self.time_casa else None
        visitante = self.time_visitante if self.time_visitante else None
        data_value = self.data.date() if self.data else ""
        if casa and visitante:
            return f"{casa} x {visitante} - {data_value}"
        elif self.adversario:
            return f"{self.adversario} - {data_value}"
        else:
            return f"Partida em {data_value}"

# -----------------------
# Modelo: Gol
# -----------------------
class Gol(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name='gols')
    autor = models.ForeignKey(Jogador, on_delete=models.SET_NULL, null=True, blank=True)
    minuto = models.PositiveIntegerField(help_text="Minuto do gol", null=True, blank=True)
    def __str__(self):
        autor_nome = self.autor.nome if self.autor is not None else "Autor desconhecido"
        minuto_text = f"{self.minuto}'" if self.minuto is not None else "minuto desconhecido"
        return f"Gol de {autor_nome} aos {minuto_text} - {self.partida}"

# -----------------------
# Modelo: AvaliacaoPartida (SUA PARTE)
# -----------------------
class AvaliacaoPartida(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name='avaliacoes')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nota = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Nota da partida (0 a 5)"
    )
    melhor_jogador = models.ForeignKey(Jogador, on_delete=models.SET_NULL, null=True, blank=True, related_name='melhor_em_avaliacoes')
    pior_jogador = models.ForeignKey(Jogador, on_delete=models.SET_NULL, null=True, blank=True, related_name='pior_em_avaliacoes')
    comentario_avaliacao = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        usuario_text = self.usuario.username if self.usuario and hasattr(self.usuario, 'username') else "Anônimo"
        return f"Avaliação ({self.nota}) por {usuario_text} - {self.partida}"
