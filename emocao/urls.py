from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='emocao_index'),
    path('avaliacao/nova/', views.nova_avaliacao, name='nova_avaliacao'),
    # Atribui ao caminho a rota de 'avaliacao/nova/' sugerindo uma página de nova avaliação, que seja procurada nas 'views' dentro da função 'nova_avaliacao', irá também usar o nome 'nova_avaliacao' para facilitar as buscas 
    #    Define a rota para a página de avaliação.
    #    'avaliar/<int:time_id>/': Captura um número inteiro da URL e o passa como argumento 'time_id' para a view.
    #    views.avaliar_time: Especifica que esta rota deve chamar a função 'avaliar_time' em views.py.
    #    name='avaliar_time': Dá um nome único à rota, facilitando o uso em redirects e templates.
    path('avaliar/<int:time_id>/', views.avaliar_time, name='avaliar_time'),

    #    Define a rota para a página de resultados.
    #    'resultado/': URL estática para a página de listagem.
    #    views.resultado_avaliacoes: Conecta esta rota à view 'resultado_avaliacoes'.
    #    name='resultado_avaliacoes': Nomeia a rota para referência futura.
    path('resultado/', views.resultado_avaliacoes, name='resultado_avaliacoes'),
]