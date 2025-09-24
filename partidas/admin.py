from django.contrib import admin
from .models import Partida, Time, Gol, AvaliacaoPartida, Jogador

# Inline para Gol dentro da Partida (útil para visualizar/editar os gols vinculados)
class GolInline(admin.TabularInline):
    model = Gol
    extra = 0
    fields = ['autor', 'minuto']
    show_change_link = True

# Inline para AvaliacaoPartida (mostra avaliações na página da Partida)
class AvaliacaoPartidaInline(admin.TabularInline):
    model = AvaliacaoPartida
    extra = 0
    fields = ['usuario', 'nota', 'melhor_jogador', 'pior_jogador', 'created_at']
    readonly_fields = ['created_at']
    show_change_link = True

class PartidaAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at']
    list_filter = ['data']
    search_fields = ['adversario', 'time_casa__nome', 'time_visitante__nome']
    inlines = [GolInline, AvaliacaoPartidaInline]

class TimeAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']

class JogadorAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']

class AvaliacaoPartidaAdmin(admin.ModelAdmin):
    list_display = ['partida', 'usuario', 'nota', 'created_at']
    list_filter = ['nota', 'created_at']
    search_fields = ['usuario__username', 'comentario']

admin.site.register(Partida, PartidaAdmin)
admin.site.register(Time, TimeAdmin)
admin.site.register(Jogador, JogadorAdmin)
admin.site.register(AvaliacaoPartida, AvaliacaoPartidaAdmin)
admin.site.register(Gol)  # opcional, se quiser gerenciar gols diretamente
