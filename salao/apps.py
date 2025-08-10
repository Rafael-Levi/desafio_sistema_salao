from django.apps import AppConfig

class SalaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'salao'

    def ready(self):
        try:
          import salao.signals
        except Exception:
            pass