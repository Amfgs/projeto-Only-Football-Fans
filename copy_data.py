from django.apps import apps
from django.db import transaction

# Modelos antigos
OldHist = apps.get_model('partidas', 'HistoricoPartida')
OldDef = apps.get_model('midia', 'Definicao')
OldImg = apps.get_model('midia', 'Imagem')
OldVideo = apps.get_model('midia', 'Video')
OldAudio = apps.get_model('midia', 'Audio')

# Modelos novos no core
NewHist = apps.get_model('core', 'HistoricoPartida')
NewDef = apps.get_model('core', 'Definicao')
NewImg = apps.get_model('core', 'Imagem')
NewVideo = apps.get_model('core', 'Video')
NewAudio = apps.get_model('core', 'Audio')

# Dicionários para mapear IDs antigos -> novos
old_to_new_hist = {}
old_to_new_def = {}

# Transação atômica para copiar todos os dados
with transaction.atomic():
    # Copiar Histórico de partidas
    for o in OldHist.objects.all():
        n = NewHist.objects.create(
            usuario=o.usuario,
            time_id=o.time_id,
            nota=o.nota,
            data=o.data
        )
        old_to_new_hist[o.pk] = n.pk

    # Copiar Definição de mídia
    for od in OldDef.objects.all():
        new_jogo_pk = old_to_new_hist.get(od.jogo_id)
        n = NewDef.objects.create(
            jogo_id=new_jogo_pk,
            descricao=od.descricao,
            criado_em=od.criado_em
        )
        old_to_new_def[od.pk] = n.pk

    # Copiar Imagens
    for oi in OldImg.objects.all():
        NewImg.objects.create(
            definicao_id=old_to_new_def[oi.definicao_id],
            arquivo=oi.arquivo,
            criado_em=oi.criado_em
        )

    # Copiar Vídeos
    for ov in OldVideo.objects.all():
        NewVideo.objects.create(
            definicao_id=old_to_new_def[ov.definicao_id],
            arquivo=ov.arquivo,
            criado_em=ov.criado_em
        )

    # Copiar Áudios
    for oa in OldAudio.objects.all():
        NewAudio.objects.create(
            definicao_id=old_to_new_def[oa.definicao_id],
            arquivo=oa.arquivo,
            criado_em=oa.criado_em
        )
