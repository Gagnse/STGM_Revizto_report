import os
import sys
import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        Initialize the Revizto API when the app starts.
        """
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
            licence_uuid = getattr(settings, 'REVIZTO_LICENCE_UUID', None)

            if access_token and refresh_token and licence_uuid:
                # Initialize the API client with tokens and licence UUID
                ReviztoAPI.initialize(access_token, refresh_token)
                print("Revizto API client initialized with tokens")

                # Set the licence UUID
                ReviztoAPI.LICENCE_UUID = licence_uuid
                print(f"Revizto Licence UUID set to: {licence_uuid}")

                # Verify token validity immediately
                if ReviztoAPI.ensure_token_valid():
                    print("Revizto API token verified as valid")
                else:
                    print("WARNING: Revizto API token could not be verified")

                # Try a test connection
                if ReviztoAPI.test_connection():
                    print("Revizto API connection test successful")
                else:
                    print("WARNING: Revizto API connection test failed")

                # Start the token refresher if enabled
                if getattr(settings, 'REVIZTO_ENABLE_TOKEN_REFRESH', True):
                    token_refresher.initialize(ReviztoAPI)
                    print("Revizto API token refresher started")
                else:
                    print("Revizto API token auto-refresh is disabled")
            else:
                print("Warning: Revizto API tokens not configured in settings")
                if not access_token:
                    print("- Missing REVIZTO_ACCESS_TOKEN")
                if not refresh_token:
                    print("- Missing REVIZTO_REFRESH_TOKEN")
                if not licence_uuid:
                    print("- Missing REVIZTO_LICENCE_UUID")
        except Exception as e:
            import traceback
            print(f"Error initializing Revizto API client: {e}")
            print(f"Traceback: {traceback.format_exc()}")