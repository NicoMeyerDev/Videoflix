from django.apps import AppConfig


class ContentConfig(AppConfig):
    name = 'videoflix_app'

    def ready(self):
        import videoflix_app.signals
