from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """
    Configure profiles app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        import profiles.signals
