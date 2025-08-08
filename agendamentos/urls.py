from django.urls import path
from . import views
from .views import relatorio_servicos
app_name = 'agendamentos'

urlpatterns = [
    path('', views.AgendamentoListView.as_view(), name='list'),
    path('novo/', views.AgendamentoCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', views.AgendamentoUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.AgendamentoDeleteView.as_view(), name='delete'),
    path('<int:pk>/', views.AgendamentoDetailView.as_view(), name='detail'),
    path('relatorio/servicos/', relatorio_servicos, name='relatorio_servicos'),
]
