from django.contrib import admin
from django.utils.html import format_html
from .models import Partida, Time, AvaliacaoEstadio, Registro

# Inline para AvaliacaoEstadio dentro da Partida
class AvaliacaoEstadioInline(admin.TabularInline):
    model = AvaliacaoEstadio
    extra = 0
    fields = ['usuario', 'tipo_emocao', 'intensidade', 'avaliacao_experiencia', 'comentario']
    show_change_link = True  # permite editar no popup

# Inline para Registro/Presença dentro da Partida
class RegistroInline(admin.TabularInline):
    model = Registro
    extra = 0
    fields = ['usuario', 'compareceu']
    show_change_link = True  # popup para editar

# Admin de Partida
class PartidaAdmin(admin.ModelAdmin):
    list_display = [
        'time_casa', 
        'time_visitante', 
        'gols_casa', 
        'placar_adv', 
        'compareceu_total', 
        'data'
    ]
    
    list_filter = [
        'time_casa', 
        'time_visitante', 
        'data'
    ]
    
    search_fields = [
        'time_casa__nome', 
        'time_visitante__nome'
    ]
    
    inlines = [AvaliacaoEstadioInline, RegistroInline]

    # Método para mostrar placar do visitante
    def placar_adv(self, obj):
        return obj.gols_visitante
    placar_adv.short_description = "Placar Visitante"
    
    # Método para mostrar presença total de participantes
    def compareceu_total(self, obj):
        return obj.registro_set.filter(compareceu=True).count()
    compareceu_total.short_description = "Compareceram"

# Admin de Time
class TimeAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']

# Admin de AvaliacaoEstadio (opcional standalone)
class AvaliacaoEstadioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'partida', 'tipo_emocao', 'intensidade', 'avaliacao_experiencia']
    list_filter = ['tipo_emocao', 'avaliacao_experiencia']
    search_fields = ['usuario__username', 'comentario']

# Admin de Registro (opcional standalone)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'partida', 'compareceu']
    list_filter = ['compareceu']
    search_fields = ['usuario__username']

# Registrando modelos no admin
admin.site.register(Partida, PartidaAdmin)
admin.site.register(Time, TimeAdmin)
admin.site.register(AvaliacaoEstadio, AvaliacaoEstadioAdmin)
admin.site.register(Registro, RegistroAdmin)
