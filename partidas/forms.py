from django import forms
from .models import Partida, Jogador

class PartidaForm(forms.ModelForm):
    data = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type':'datetime-local'}),
        label='Data e hora da partida'
    )

    class Meta:
        model = Partida
        fields = ['adversario', 'data', 'placar_time', 'placar_adversario']

class AvaliacaoPartidaForm(forms.ModelForm):
    class Meta:
        model = Partida
        fields = ['nota', 'melhor_jogador', 'pior_jogador']
        widgets = {
            'nota': forms.NumberInput(attrs={'min':0, 'max':5}),
        }
