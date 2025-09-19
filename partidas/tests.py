from django.test import TestCase
from .models import Historico  # ou Partida, depende do nome do seu model

class HistoricoModelTest(TestCase):
    def test_str_retorna_legivel(self):
        # cria uma partida/histórico só em memória
        h = Historico(
            data="2025-01-01",
            adversario="Time Teste",
            placar_time=2,
            placar_adv=1,
            nota=8,
        )
        # garante que o __str__ retorna um texto
        self.assertIn("Time Teste", str(h))

