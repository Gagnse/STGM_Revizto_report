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
            # Import the token manager first to avoid circular imports
            from .api.token_manager import TokenManager
            from .api.client import ReviztoAPI

            # Initialize the TokenManager, which will load tokens from environment variables
            print("Initializing Revizto API token manager...")
            TokenManager.initialize()

            # Initialize the API client
            ReviztoAPI.initialize()
            print("Revizto API client initialized")
        except Exception as e:
            print(f"Error initializing Revizto API client: {e}")