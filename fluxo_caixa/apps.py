from django.apps import AppConfig


class FluxoCaixaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fluxo_caixa'

    def ready(self):
        import fluxo_caixa.signals
