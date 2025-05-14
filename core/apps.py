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

        print("\n====== REVIZTO API INITIALIZATION ======")

        try:
            from django.conf import settings
            from .api.client import ReviztoAPI

            # CRITICAL CHANGE: Set tokens directly first, before anything else
            ReviztoAPI.ACCESS_TOKEN = settings.REVIZTO_ACCESS_TOKEN
            ReviztoAPI.REFRESH_TOKEN = settings.REVIZTO_REFRESH_TOKEN
            ReviztoAPI.LICENCE_UUID = settings.REVIZTO_LICENCE_UUID

            # Set token expiry to current time + 1 hour
            from datetime import datetime, timedelta
            ReviztoAPI.TOKEN_EXPIRY = datetime.now() + timedelta(seconds=3600)

            # Debug the token state after direct setting
            print(f"DIRECT TOKEN SETTING:")
            print(
                f"- Access token set: {'YES' if ReviztoAPI.ACCESS_TOKEN else 'NO'} (Length: {len(ReviztoAPI.ACCESS_TOKEN) if ReviztoAPI.ACCESS_TOKEN else 0})")
            print(
                f"- Refresh token set: {'YES' if ReviztoAPI.REFRESH_TOKEN else 'NO'} (Length: {len(ReviztoAPI.REFRESH_TOKEN) if ReviztoAPI.REFRESH_TOKEN else 0})")
            print(
                f"- License UUID set: {'YES' if ReviztoAPI.LICENCE_UUID else 'NO'} (Length: {len(ReviztoAPI.LICENCE_UUID) if ReviztoAPI.LICENCE_UUID else 0})")

            # Import token refresher after settings tokens
            from .api import token_refresher

            # Only proceed with usual initialization if tokens exist
            if ReviztoAPI.ACCESS_TOKEN and ReviztoAPI.REFRESH_TOKEN and ReviztoAPI.LICENCE_UUID:
                print("All required tokens are available, proceeding with API initialization")

                # Verify token validity immediately
                if ReviztoAPI.ensure_token_valid():
                    print("Revizto API token verified as valid")
                else:
                    print("WARNING: Revizto API token could not be verified")

                # Start the token refresher if enabled
                if getattr(settings, 'REVIZTO_ENABLE_TOKEN_REFRESH', True):
                    token_refresher.initialize(ReviztoAPI)
                    print("Revizto API token refresher started")
                else:
                    print("Revizto API token auto-refresh is disabled")
            else:
                print("CRITICAL: Not all required tokens are available after direct setting")
                if not ReviztoAPI.ACCESS_TOKEN:
                    print("- Missing ACCESS_TOKEN")
                if not ReviztoAPI.REFRESH_TOKEN:
                    print("- Missing REFRESH_TOKEN")
                if not ReviztoAPI.LICENCE_UUID:
                    print("- Missing LICENCE_UUID")
        except Exception as e:
            import traceback
            print(f"CRITICAL: Error initializing Revizto API client: {e}")
            print(f"Traceback: {traceback.format_exc()}")

        print("====== REVIZTO API INITIALIZATION COMPLETE ======\n")