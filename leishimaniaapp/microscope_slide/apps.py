from django.apps import AppConfig


class MicroscopeSlideConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "leishimaniaapp.microscope_slide"

    def ready(self):
        import leishimaniaapp.microscope_slide.signals
