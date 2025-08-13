from django.contrib import admin
from django.urls import path,include
from .admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('agendamentos/', include('salao.routers.agendamento_urls', namespace='agendamentos')),
    path('clientes/', include('salao.routers.cliente_urls', namespace='clientes')),
    path('relatorios/', include('salao.routers.relatorio_urls', namespace='relatorios')),
    path('', include('salao.routers.login_urls', namespace='login'))
]

