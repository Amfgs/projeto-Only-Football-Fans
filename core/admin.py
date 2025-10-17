from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario,
    Definicao, Imagem, Video, Audio, Link,
    Partida, Jogador, Gol,
    AvaliacaoPartida, AvaliacaoEstadio, AvaliacaoTorcida,
    Time, HistoricoPartida
)

# --- Usuário customizado ---
@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    # Campos extras nas telas do admin
    fieldsets = UserAdmin.fieldsets + (
        ('Informações adicionais', {'fields': ('time_favorito', 'pais', 'avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações adicionais', {'fields': ('time_favorito', 'pais', 'avatar')}),
    )
    list_display = ('username', 'email', 'time_favorito', 'pais', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'time_favorito', 'pais')

# --- Demais modelos (registro simples) ---
@admin.register(Definicao)
class DefinicaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'jogo', 'descricao', 'criado_em')
    search_fields = ('jogo', 'descricao', 'usuario__username')
    list_filter = ('criado_em',)

@admin.register(Imagem)
class ImagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'definicao', 'arquivo', 'thumbnail', 'criado_em')
    list_filter = ('criado_em',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'definicao', 'arquivo', 'criado_em')
    list_filter = ('criado_em',)

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('id', 'definicao', 'arquivo', 'criado_em')
    list_filter = ('criado_em',)

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_do_jogo', 'titulo', 'url', 'definicao', 'criado_em')
    search_fields = ('nome_do_jogo', 'titulo', 'url')
    list_filter = ('criado_em',)

@admin.register(Jogador)
class JogadorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'time_casa', 'time_visitante', 'adversario', 'data', 'created_at')
    list_filter = ('data', 'created_at')
    search_fields = ('time_casa', 'time_visitante', 'adversario', 'usuario__username')

@admin.register(Gol)
class GolAdmin(admin.ModelAdmin):
    list_display = ('id', 'partida', 'autor', 'minuto')
    list_filter = ('minuto',)

@admin.register(AvaliacaoPartida)
class AvaliacaoPartidaAdmin(admin.ModelAdmin):
    list_display = ('id', 'partida', 'usuario', 'nota', 'melhor_jogador', 'pior_jogador', 'created_at')
    list_filter = ('nota', 'created_at')
    search_fields = ('partida__time_casa', 'partida__time_visitante', 'usuario__username')

@admin.register(AvaliacaoEstadio)
class AvaliacaoEstadioAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'estadio', 'avaliacao_experiencia', 'data_avaliacao')
    list_filter = ('avaliacao_experiencia', 'data_avaliacao')
    search_fields = ('usuario__username', 'estadio')

@admin.register(AvaliacaoTorcida)
class AvaliacaoTorcidaAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'emocao', 'presenca', 'data_criacao')
    list_filter = ('emocao', 'presenca', 'data_criacao')
    search_fields = ('time',)

@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

@admin.register(HistoricoPartida)
class HistoricoPartidaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'time_id', 'nota', 'data')
    list_filter = ('data', 'nota')
    search_fields = ('usuario',)
