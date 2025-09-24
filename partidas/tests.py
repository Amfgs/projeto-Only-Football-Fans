from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Partida, Jogador, Gol, AvaliacaoPartida

User = get_user_model()

class PartidaModelTest(TestCase):
    def test_str_retorna_texto_correto(self):
        partida = Partida.objects.create(adversario="Time Teste", data=timezone.now())
        self.assertIn("Time Teste", str(partida))

class AvaliacaoPartidaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='12345')
        self.jog = Jogador.objects.create(nome="João")
        self.partida = Partida.objects.create(adversario="Time Teste", data=timezone.now())

    def test_avaliacao_e_gol_criacao(self):
        # cria avaliação
        aval = AvaliacaoPartida.objects.create(
            partida=self.partida,
            usuario=self.user,
            nota=4,
            melhor_jogador=self.jog,
            pior_jogador=self.jog,
            comentario="Bom jogo"
        )
        # cria gol
        gol = Gol.objects.create(partida=self.partida, autor=self.jog, minuto=23)

        self.assertIn("Time Teste", str(self.partida))
        self.assertEqual(str(self.jog), "João")
        self.assertIn("João", str(gol))
        self.assertEqual(aval.nota, 4)
