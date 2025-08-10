from django.contrib.auth.models import Group, Permission, User
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from .models.profissional import Profissional

@receiver(post_migrate)
def criar_grupos_e_permissoes(sender, **kwargs):
    if sender.name != 'salao':
        return

    dono_group, _ = Group.objects.get_or_create(name='Dono')
    recep_group, _ = Group.objects.get_or_create(name='Recepcionista')
    prof_group, _ = Group.objects.get_or_create(name='Profissional')

    codes_recepc = [
        'add_agendamento','change_agendamento','delete_agendamento','view_agendamento',
        'add_cliente','change_cliente','delete_cliente','view_cliente',
    ]
    recep_perms = Permission.objects.filter(codename__in=codes_recepc)
    recep_group.permissions.set(recep_perms)

    prof_perms = Permission.objects.filter(codename__in=['view_agendamento','view_cliente','change_agendamento'])
    prof_group.permissions.set(prof_perms)

    dono_group.permissions.set(Permission.objects.all())

    print("Grupos (Dono, Recepcionista, Profissional) verificados/criados e permissões atribuídas.")


@receiver(post_save, sender=Profissional)
def on_profissional_saved(sender, instance, created, **kwargs):
    if instance.user:
        prof_group, _ = Group.objects.get_or_create(name='Profissional')
        instance.user.groups.add(prof_group)


@receiver(post_save, sender=User)
def ensure_profissional_for_user(sender, instance, created, **kwargs):
    if instance.groups.filter(name='Profissional').exists():
        try:
            Profissional.objects.get(user=instance)
        except Profissional.DoesNotExist:
            Profissional.objects.create(user=instance, nome=instance.get_full_name() or instance.username)
