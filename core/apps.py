# core/apps.py - Replace your existing file

import os
import sys
import logging
import threading
from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger(__name__)


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """Initialize the Revizto API when the app starts."""
        # Avoid running during migrations or when collecting static files
        if any(cmd in sys.argv for cmd in ['migrate', 'collectstatic', 'makemigrations']):
            logger.info("Skipping API initialization during Django management command")
            return

        # Skip in certain test environments
        if 'test' in sys.argv or os.environ.get('DJANGO_TESTING'):
            logger.info("Skipping API initialization during testing")
            return

        # Check if this is a web process (not a one-off dyno)
        if not ('runserver' in sys.argv or 'gunicorn' in sys.argv[0] or os.environ.get('DYNO')):
            logger.info("Skipping API initialization (not in web process)")
            return

        # Avoid running in Django's auto-reload cycles
        if os.environ.get('RUN_MAIN') != 'true' and 'runserver' in sys.argv:
            logger.info("Skipping API initialization (Django auto-reloader)")
            return

        print("\n" + "=" * 60)
        print("🚀 REVIZTO API INITIALIZATION - ENHANCED VERSION")
        print("=" * 60)

        # Initialize in a separate thread to avoid blocking Django startup
        threading.Thread(target=self._initialize_api, daemon=True).start()

    def _initialize_api(self):
        """Initialize the API in a separate thread."""
        try:
            # Import here to avoid circular imports
            from .api.client import ReviztoAPI
            from .api import token_store, token_refresher
            from .models import TokenStorage

            # Ensure database is ready
            self._ensure_database_ready()

            # Get tokens from settings
            access_token = getattr(settings, 'REVIZTO_ACCESS_TOKEN', '')
            refresh_token = getattr(settings, 'REVIZTO_REFRESH_TOKEN', '')
            licence_uuid = getattr(settings, 'REVIZTO_LICENCE_UUID', '')

            print(f"📊 TOKEN STATUS FROM SETTINGS:")
            print(f"   Access token: {'✅ Present' if access_token else '❌ Missing'} ({len(access_token)} chars)")
            print(f"   Refresh token: {'✅ Present' if refresh_token else '❌ Missing'} ({len(refresh_token)} chars)")
            print(f"   License UUID: {'✅ Present' if licence_uuid else '❌ Missing'} ({len(licence_uuid)} chars)")

            if not all([access_token, refresh_token, licence_uuid]):
                print("❌ CRITICAL: Missing required tokens in settings")
                self._log_token_sources()
                return

            # Check if we have existing tokens in database
            existing_tokens = token_store.has_tokens()
            print(f"💾 DATABASE TOKEN STATUS: {'✅ Present' if existing_tokens else '❌ Missing'}")

            if existing_tokens:
                print("🔄 Found existing tokens in database, checking validity...")

                # Check if existing tokens are valid
                if not token_store.is_token_expired():
                    print("✅ Existing tokens are still valid")

                    # Test API connection
                    if ReviztoAPI.test_connection():
                        print("✅ API connection test successful")
                    else:
                        print("⚠️  API connection test failed, refreshing tokens...")
                        ReviztoAPI.refresh_token()
                else:
                    print("⚠️  Existing tokens are expired, refreshing...")
                    ReviztoAPI.refresh_token()
            else:
                print("🔄 No existing tokens in database, initializing from settings...")
                ReviztoAPI.initialize(access_token, refresh_token, licence_uuid)

            # Verify token validity after initialization
            if ReviztoAPI.ensure_token_valid():
                print("✅ Token verification successful")
            else:
                print("❌ Token verification failed")

            # Start the enhanced token refresher
            if getattr(settings, 'REVIZTO_ENABLE_TOKEN_REFRESH', True):
                print("🔄 Starting enhanced token refresher...")
                if token_refresher.initialize(ReviztoAPI):
                    print("✅ Token refresher started successfully")

                    # Get refresher status
                    status = token_refresher.get_status()
                    print(f"📊 Refresher Status:")
                    print(f"   Environment: {'Heroku' if status.get('is_heroku') else 'Local'}")
                    print(f"   Dyno ID: {status.get('dyno_id', 'unknown')}")
                    print(f"   Thread alive: {status.get('thread_alive', False)}")
                else:
                    print("❌ Failed to start token refresher")
            else:
                print("⚠️  Token auto-refresh is disabled in settings")

            # Final API connection test
            print("🧪 Performing final API connection test...")
            if ReviztoAPI.test_connection():
                print("✅ INITIALIZATION COMPLETE - API Ready!")
            else:
                print("❌ INITIALIZATION WARNING - API connection issues detected")

            print("=" * 60)
            print("🎉 REVIZTO API INITIALIZATION FINISHED")
            print("=" * 60 + "\n")

        except Exception as e:
            import traceback
            print(f"❌ CRITICAL ERROR during API initialization: {e}")
            print(f"📜 Traceback: {traceback.format_exc()}")
            print("=" * 60 + "\n")

    def _ensure_database_ready(self):
        """Ensure the database and required tables are ready."""
        try:
            from django.db import connection
            from .models import TokenStorage

            # Test database connection
            connection.ensure_connection()

            # Ensure TokenStorage table exists
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='revizto_tokens'
                """)

                if not cursor.fetchone():
                    print("⚠️  TokenStorage table not found, creating...")
                    # Run migrations for our model
                    from django.core.management import execute_from_command_line
                    execute_from_command_line(['manage.py', 'migrate', 'core', '--run-syncdb'])
                    print("✅ TokenStorage table created")

        except Exception as e:
            logger.warning(f"Database readiness check failed: {e}")

    def _log_token_sources(self):
        """Log information about where tokens should come from."""
        print("\n🔍 TOKEN SOURCE DEBUGGING:")

        # Check environment variables
        env_vars = ['REVIZTO_ACCESS_TOKEN', 'REVIZTO_REFRESH_TOKEN', 'REVIZTO_LICENCE_UUID']
        for var in env_vars:
            value = os.environ.get(var, '')
            print(f"   ENV {var}: {'✅ Set' if value else '❌ Missing'} ({len(value)} chars)")

        # Check if running on Heroku
        if os.environ.get('DYNO'):
            print(f"   🏢 Running on Heroku dyno: {os.environ.get('DYNO')}")
            print("   💡 Ensure config vars are set in Heroku dashboard")
        else:
            print("   💻 Running locally")
            print("   💡 Check .env file or environment variables")

        print("")