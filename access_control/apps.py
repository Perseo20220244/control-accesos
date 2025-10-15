from django.apps import AppConfig


class AccessControlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'access_control'
    verbose_name = 'Control de Accesos'
    
    def ready(self):
        """Importar signals cuando la app esté lista"""
        import access_control.signals
