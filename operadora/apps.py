from django.apps import AppConfig

class OperadoraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'operadora'

    def ready(self):
        print("🚀 apps.py: Executando ready()")
        import operadora.signals
