from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        Initialize the Revizto API when the app starts.
        """
        import os
        import sys

        # Avoid running this during migrations or when collecting static files
        if 'runserver' not in sys.argv and 'manage.py' not in sys.argv:
            return

        # Also avoid running in auto-reload cycles
        if os.environ.get('RUN_MAIN') != 'true' and 'runserver' in sys.argv:
            return

        try:
            from django.conf import settings
            from .api.client import ReviztoAPI
            # Import our token refresher
            from .api import token_refresher

            # Get tokens from settings
            access_token = getattr(settings, 'REVIZTO_ACCESS_TOKEN', None)
            refresh_token = getattr(settings, 'REVIZTO_REFRESH_TOKEN', None)

            if access_token and refresh_token:
                # Initialize the API client with tokens
                ReviztoAPI.initialize(access_token, refresh_token)
                print("Revizto API client initialized")

                # Start the token refresher
                token_refresher.initialize(ReviztoAPI)
                print("Revizto API token refresher started - tokens will refresh every 30 minutes")
            else:
                print("Warning: Revizto API tokens not configured in settings")
        except Exception as e:
            print(f"Error initializing Revizto API client: {e}")