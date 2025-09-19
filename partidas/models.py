from django.db import models
from django.utils import timezone

class HistoricoPartida(models.Model):
    usuario = models.CharField(max_length=200)
    time_id = models.IntegerField()
    nota = models.IntegerField()
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario} - Time {self.time_id} - Nota {self.nota}"
