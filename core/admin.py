from django.contrib import admin
from salao.models import profissional, agendamento, cliente,servico

class CustomAdminSite(admin.AdminSite):
    site_header = "Salão de beleza backoffice"

admin_site = CustomAdminSite()
admin_site.register(profissional.Profissional)
admin_site.register(agendamento.Agendamento)
admin_site.register(cliente.Cliente)
admin_site.register(servico.Servico)