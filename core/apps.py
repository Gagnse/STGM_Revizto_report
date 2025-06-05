# core/apps.py - Fixed version with proper PostgreSQL integration

import os
import sys
import logging
import threading
import time
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
        print("🚀 REVIZTO API INITIALIZATION - POSTGRESQL VERSION")
        print("=" * 60)

        # Initialize in a separate thread to avoid blocking Django startup
        threading.Thread(target=self._initialize_api, daemon=True).start()

    def _initialize_api(self):
        """Initialize the API in a separate thread."""
        try:
            # Wait a moment for Django to fully start
            time.sleep(2)

            # Import here to avoid circular imports
            from .api.client import ReviztoAPI
            from .api import token_store, token_refresher

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

            # Check if we have existing tokens in PostgreSQL database
            print("🔍 Checking PostgreSQL database for existing tokens...")
            existing_tokens = token_store.has_tokens()
            print(f"💾 POSTGRESQL TOKEN STATUS: {'✅ Present' if existing_tokens else '❌ Missing'}")

            if existing_tokens:
                print("🔄 Found existing tokens in PostgreSQL, checking validity...")

                # Check if existing tokens are valid
                if not token_store.is_token_expired():
                    print("✅ Existing tokens in PostgreSQL are still valid")

                    # Test API connection with existing tokens
                    if ReviztoAPI.test_connection():
                        print("✅ API connection test successful with PostgreSQL tokens")
                    else:
                        print("⚠️  API connection test failed, refreshing tokens...")
                        if ReviztoAPI.refresh_token():
                            print("✅ Token refresh successful")
                        else:
                            print("❌ Token refresh failed, reinitializing from settings...")
                            ReviztoAPI.initialize(access_token, refresh_token, licence_uuid)
                else:
                    print("⚠️  Existing tokens in PostgreSQL are expired, refreshing...")
                    if ReviztoAPI.refresh_token():
                        print("✅ Token refresh successful")
                    else:
                        print("❌ Token refresh failed, reinitializing from settings...")
                        ReviztoAPI.initialize(access_token, refresh_token, licence_uuid)
            else:
                print("🔄 No existing tokens in PostgreSQL, initializing from settings...")
                if ReviztoAPI.initialize(access_token, refresh_token, licence_uuid):
                    print("✅ Successfully initialized tokens in PostgreSQL from settings")
                else:
                    print("❌ Failed to initialize tokens in PostgreSQL")
                    return

            # Verify token validity after initialization
            print("🧪 Verifying token validity...")
            if ReviztoAPI.ensure_token_valid():
                print("✅ Token verification successful")
            else:
                print("❌ Token verification failed")

            # Display final token status
            print("📊 FINAL TOKEN STATUS:")
            status = token_store.get_token_status()
            if 'error' not in status:
                print(f"   PostgreSQL Storage: ✅ Connected")
                print(
                    f"   Access Token: {'✅' if status['has_access_token'] else '❌'} ({status['access_token_length']} chars)")
                print(
                    f"   Refresh Token: {'✅' if status['has_refresh_token'] else '❌'} ({status['refresh_token_length']} chars)")
                print(f"   License UUID: {'✅' if status['has_licence_uuid'] else '❌'}")
                print(f"   Token Expired: {'🔴 Yes' if status['is_expired'] else '🟢 No'}")
                print(f"   Last Refresh: {status['last_successful_refresh'] or 'Never'}")
            else:
                print(f"   ❌ Error getting status: {status['error']}")

            # Start the enhanced token refresher
            if getattr(settings, 'REVIZTO_ENABLE_TOKEN_REFRESH', True):
                print("🔄 Starting enhanced token refresher...")
                if token_refresher.initialize(ReviztoAPI):
                    print("✅ Token refresher started successfully")

                    # Get refresher status
                    refresher_status = token_refresher.get_status()
                    print(f"📊 Refresher Status:")
                    print(f"   Environment: {'Heroku' if refresher_status.get('is_heroku') else 'Local'}")
                    print(f"   Dyno ID: {refresher_status.get('dyno_id', 'unknown')}")
                    print(f"   Thread alive: {refresher_status.get('thread_alive', False)}")
                else:
                    print("❌ Failed to start token refresher")
            else:
                print("⚠️  Token auto-refresh is disabled in settings")

            # Final API connection test
            print("🧪 Performing final API connection test...")
            if ReviztoAPI.test_connection():
                print("✅ INITIALIZATION COMPLETE - API Ready!")
                print("💾 Tokens are now persisted in PostgreSQL database")
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
        """Ensure the PostgreSQL database and required tables are ready."""
        try:
            print("🔧 Ensuring PostgreSQL database is ready...")

            # Test PostgreSQL connection
            from django.db import connections
            postgres_conn = connections['postgres']

            # Test the connection
            postgres_conn.ensure_connection()
            print("✅ PostgreSQL connection established")

            # Check if TokenStorage table exists and create if needed
            with postgres_conn.cursor() as cursor:
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = 'revizto_tokens'
                    );
                """)

                table_exists = cursor.fetchone()[0]

                if not table_exists:
                    print("⚠️  revizto_tokens table not found in PostgreSQL, creating...")
                    cursor.execute("""
                        CREATE TABLE revizto_tokens (
                            id SERIAL PRIMARY KEY,
                            access_token TEXT,
                            refresh_token TEXT,
                            licence_uuid VARCHAR(255),
                            token_expiry TIMESTAMP WITH TIME ZONE,
                            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                            last_refresh_attempt TIMESTAMP WITH TIME ZONE,
                            last_successful_refresh TIMESTAMP WITH TIME ZONE,
                            refresh_failure_count INTEGER DEFAULT 0
                        );
                    """)
                    print("✅ revizto_tokens table created in PostgreSQL")
                else:
                    print("✅ revizto_tokens table already exists in PostgreSQL")

        except Exception as e:
            print(f"❌ PostgreSQL database readiness check failed: {e}")
            import traceback
            print(f"📜 Traceback: {traceback.format_exc()}")

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