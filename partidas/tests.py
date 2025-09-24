from django.test import TestCase
from .models import Historico  # ou Partida, depende do nome do seu model

from .models import Partida, Jogador, Gol
from django.utils import timezone

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

class PartidaModelTest(TestCase):
    def test_str_retorna_texto_correto(self):
        jogador = Jogador.objects.create(nome="João")
        partida = Partida.objects.create(
            adversario="Time Teste",
            data=timezone.now(),
            placar_time=3,
            placar_adversario=1,
            nota=4,
            melhor_jogador=jogador,
            pior_jogador=jogador
        )
        gol = Gol.objects.create(partida=partida, autor=jogador, minuto=23)

        self.assertIn("Time Teste", str(partida))
        self.assertEqual(str(jogador), "João")
        self.assertIn("João", str(gol))
