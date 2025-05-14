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
        if 'runserver' not in sys.argv and 'gunicorn' not in sys.argv[0]:
            logger.info("Skipping API initialization (not in runserver or gunicorn)")
            return

        # Also avoid running in auto-reload cycles
        if os.environ.get('RUN_MAIN') != 'true' and 'runserver' in sys.argv:
            logger.info("Skipping API initialization (development reloader)")
            return

        print("\n====== REVIZTO API INITIALIZATION ======")

        try:
            from django.conf import settings
            from .api.client import ReviztoAPI
            from .api import token_store

            # Get tokens from settings
            access_token = settings.REVIZTO_ACCESS_TOKEN
            refresh_token = settings.REVIZTO_REFRESH_TOKEN
            licence_uuid = settings.REVIZTO_LICENCE_UUID

            # Debug tokens
            print(f"DIRECT TOKEN SETTING:")
            print(
                f"- Access token provided: {'YES' if access_token else 'NO'} (Length: {len(access_token) if access_token else 0})")
            print(
                f"- Refresh token provided: {'YES' if refresh_token else 'NO'} (Length: {len(refresh_token) if refresh_token else 0})")
            print(
                f"- License UUID provided: {'YES' if licence_uuid else 'NO'} (Length: {len(licence_uuid) if licence_uuid else 0})")

            # Initialize the API with tokens directly
            if all([access_token, refresh_token, licence_uuid]):
                print("All required tokens are available, proceeding with API initialization")

                # Initialize the client with tokens
                ReviztoAPI.initialize(access_token, refresh_token, licence_uuid)

                # Verify token validity immediately
                if ReviztoAPI.ensure_token_valid():
                    print("Revizto API token verified as valid")
                else:
                    print("WARNING: Revizto API token could not be verified")

                # Start the token refresher if enabled
                if getattr(settings, 'REVIZTO_ENABLE_TOKEN_REFRESH', True):
                    from .api import token_refresher
                    token_refresher.initialize(ReviztoAPI)
                    print("Revizto API token refresher started")
                else:
                    print("Revizto API token auto-refresh is disabled")
            else:
                print("CRITICAL: Not all required tokens are available")
                if not access_token:
                    print("- Missing ACCESS_TOKEN")
                if not refresh_token:
                    print("- Missing REFRESH_TOKEN")
                if not licence_uuid:
                    print("- Missing LICENCE_UUID")
        except Exception as e:
            import traceback
            print(f"CRITICAL: Error initializing Revizto API client: {e}")
            print(f"Traceback: {traceback.format_exc()}")

        print("====== REVIZTO API INITIALIZATION COMPLETE ======\n")