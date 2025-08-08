# agendamentos/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import relatorio_servicos

app_name = 'agendamentos'

urlpatterns = [
    # rota principal -> login
    path('', auth_views.LoginView.as_view(template_name='agendamentos/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='agendamentos:login'), name='logout'),

    # home (depois do login)
    path('home/', views.home, name='home'),

    # list/CRUD de agendamentos (mantive os nomes existentes)
    path('agendamentos/', views.AgendamentoListView.as_view(), name='list'),
    path('agendamentos/novo/', views.AgendamentoCreateView.as_view(), name='create'),
    path('agendamentos/<int:pk>/editar/', views.AgendamentoUpdateView.as_view(), name='update'),
    path('agendamentos/<int:pk>/excluir/', views.AgendamentoDeleteView.as_view(), name='delete'),
    path('agendamentos/<int:pk>/', views.AgendamentoDetailView.as_view(), name='detail'),

    # rota para mudar status (POST)
    path('agendamento/<int:pk>/status/', views.alterar_status_agendamento, name='alterar_status_agendamento'),

    # relatório
    path('relatorio/servicos/', relatorio_servicos, name='relatorio_servicos'),
]
