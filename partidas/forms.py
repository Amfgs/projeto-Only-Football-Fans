# partidas/forms.py
from django import forms
from .models import Partida, AvaliacaoPartida, Gol
from django.forms import inlineformset_factory

class PartidaForm(forms.ModelForm):
    """
    Formulário mínimo para criar/editar uma Partida.
    NOTE: se o registro da partida ficar totalmente com outro integrante,
    esse form pode ser removido (ou passado para o app de registro).
    """
    data = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label='Data e hora')

    class Meta:
        model = Partida
        # NÃO inclua campos de placar: responsabilidade do registrador
        fields = ['time_casa', 'time_visitante', 'adversario', 'data']

class AvaliacaoPartidaForm(forms.ModelForm):
    """
    Form para a sua funcionalidade principal: avaliar a partida.
    """
    class Meta:
        model = AvaliacaoPartida
        fields = ['nota', 'melhor_jogador', 'pior_jogador', 'comentario']
        widgets = {
            'nota': forms.NumberInput(attrs={'min': 0, 'max': 5}),
            'comentario': forms.Textarea(attrs={'rows': 3}),
        }

# Inline formset para Gols (autor + minuto) vinculados a uma Partida
GolFormSet = inlineformset_factory(
    Partida,
    Gol,
    fields=('autor', 'minuto'),
    extra=1,
    can_delete=True
)