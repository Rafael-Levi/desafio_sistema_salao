# agendamentos/admin.py
from django.contrib import admin
from .models import Cliente, Servico, Profissional, Agendamento

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'telefone', 'email')
    search_fields = ('nome', 'telefone', 'email')


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'duracao_minutos', 'preco')
    search_fields = ('nome',)


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'especialidade')
    search_fields = ('nome', 'especialidade')


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'servico', 'profissional', 'inicio', 'status')
    list_filter = ('status', 'profissional', 'servico')
    search_fields = ('cliente__nome', 'profissional__nome', 'servico__nome')
    ordering = ('-inicio',)
    date_hierarchy = 'inicio'
