from django.contrib import admin
from .models import agendamento,cliente,servico,profissional

@admin.register(cliente.Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'telefone', 'email')
    search_fields = ('nome', 'telefone', 'email')


@admin.register(servico.Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'duracao_minutos', 'preco')
    search_fields = ('nome',)


@admin.register(profissional.Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'user', 'especialidade')
    search_fields = ('nome', 'especialidade', 'user__username')


@admin.register(agendamento.Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'servico', 'profissional', 'inicio', 'status')
    list_filter = ('status', 'profissional', 'servico')
    search_fields = ('cliente__nome', 'profissional__nome', 'servico__nome')
    ordering = ('-inicio',)
    date_hierarchy = 'inicio'
