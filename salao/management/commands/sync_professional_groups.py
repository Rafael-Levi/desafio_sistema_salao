from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from salao.models.agendamento import Profissional

class Command(BaseCommand):
    help = 'Sincroniza grupos Profissional e cria objetos Profissional para usuários no grupo Profissional (se necessário)'

    def handle(self, *args, **options):
        prof_group, _ = Group.objects.get_or_create(name='Profissional')
        #usuários ligados a Profissional.user -> garante grupo
        count_linked = 0
        for prof in Profissional.objects.filter(user__isnull=False):
            prof.user.groups.add(prof_group)
            count_linked += 1

        #usuários no grupo Profissional -> cria Profissional se não existir
        count_created = 0
        users = User.objects.filter(groups__name='Profissional')
        for u in users:
            try:
                _ = Profissional.objects.get(user=u)
            except Profissional.DoesNotExist:
                Profissional.objects.create(user=u, nome=u.get_full_name() or u.username)
                count_created += 1

        self.stdout.write(self.style.SUCCESS(f'Users linked to Profissional group: {count_linked}'))
        self.stdout.write(self.style.SUCCESS(f'Profissional objects created for users in group: {count_created}'))
