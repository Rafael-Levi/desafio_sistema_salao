from django.urls import path
from ..views.relatorio_view import relatorio_servicos,relatorio_servicos_download

app_name = 'relatorios'

urlpatterns = [
    path('servicos/', relatorio_servicos, name='relatorio_servicos'),
    path('servicos/download/', relatorio_servicos_download, name='relatorio_servicos_download'),
]