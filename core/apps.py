from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        Initialize the Revizto API when the app starts.

        This will use the tokens from settings.py.
        """
        from .api.client import ReviztoAPI

        # Get tokens from settings
        access_token = getattr(settings, 'REVIZTO_ACCESS_TOKEN', None)
        refresh_token = getattr(settings, 'REVIZTO_REFRESH_TOKEN', None)

        if access_token and refresh_token:
            # Initialize the API client with tokens
            ReviztoAPI.initialize(access_token, refresh_token)