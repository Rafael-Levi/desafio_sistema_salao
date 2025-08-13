from django.contrib import admin
from salao.models import profissional, agendamento, cliente,servico
from django.contrib.auth.models import Group, User

class CustomAdminSite(admin.AdminSite):
    site_header = "Salão de beleza backoffice"

admin_site = CustomAdminSite()
admin_site.register(profissional.Profissional)
admin_site.register(agendamento.Agendamento)
admin_site.register(cliente.Cliente)
admin_site.register(servico.Servico)
admin_site.register(User)
admin_site.register(Group)