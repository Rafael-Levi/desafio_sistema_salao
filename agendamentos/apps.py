from django.apps import AppConfig

class AgendamentosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agendamentos'

    def ready(self):
        try:
            import agendamentos.signals  
        except Exception:
            pass