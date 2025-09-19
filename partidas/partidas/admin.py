from django.contrib import admin
from .models import Partida

@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = ("data", "adversario", "placar_time", "placar_adv", "compareceu")
    search_fields = ("adversario", "campeonato", "local")
    list_filter = ("compareceu", "campeonato", "data")
