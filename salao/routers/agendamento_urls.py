from django.urls import path
from ..views.home_view import (AgendamentoCreateView,
                               AgendamentoDeleteView,
                               AgendamentoDetailView,
                               alterar_status_agendamento,
                               AgendamentoUpdateView,
                               AgendamentoListView,
                               home)


app_name = 'agendamentos'

urlpatterns = [
    path('', home, name='home'),
    path('list/', AgendamentoListView.as_view(), name='list'),
    path('novo/', AgendamentoCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', AgendamentoUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', AgendamentoDeleteView.as_view(), name='delete'),
    path('<int:pk>/', AgendamentoDetailView.as_view(), name='detail'),
    path('<int:pk>/status/', alterar_status_agendamento, name='alterar_status_agendamento'),
]
