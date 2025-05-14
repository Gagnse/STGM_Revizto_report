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
        print(f"Current environment: {'HEROKU' if os.environ.get('DYNO') else 'LOCAL'}")

        try:
            from django.conf import settings
            from .api.client import ReviztoAPI
            # Import our token refresher
            from .api import token_refresher

            # Get tokens from settings
            access_token = getattr(settings, 'REVIZTO_ACCESS_TOKEN', None)
            refresh_token = getattr(settings, 'REVIZTO_REFRESH_TOKEN', None)
            licence_uuid = getattr(settings, 'REVIZTO_LICENCE_UUID', None)

            # Debug environment variables
            print(f"Access token available: {'YES (Length: ' + str(len(access_token)) + ')' if access_token else 'NO'}")
            print(
                f"Refresh token available: {'YES (Length: ' + str(len(refresh_token)) + ')' if refresh_token else 'NO'}")
            print(f"License UUID available: {'YES (Length: ' + str(len(licence_uuid)) + ')' if licence_uuid else 'NO'}")

            if access_token and refresh_token and licence_uuid:
                # Set tokens directly on the class, similar to how LICENCE_UUID is set
                ReviztoAPI.ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMjgzODRhYTg1M2E2YTJjYWNmMTQzZGRjNmY4MTkyZSIsImp0aSI6ImQyODNiMGYzZDE0MmNiM2Y3YjBmMmE0ODZiMGE3OGRiZjZjNDQ3OWVhZTdiMjBjZTcxNWRkMTZjMmU4NmJjOGM2Y2E1ZTYwMGQ3ZWExOTc1IiwiaWF0IjoxNzQ3MjQyMjE0LjYyMzYyNiwiaXNzIjoie1wiaG9zdFwiOlwiYXBpLmNhbmFkYS5yZXZpenRvLmNvbVwiLFwicG9ydFwiOjQ0MyxcInByb3RvY29sXCI6XCJodHRwc1wiLFwidGltZXpvbmVfbmFtZVwiOlwiQ1NUXCIsXCJ0aW1lem9uZV9zaGlmdFwiOlwiQW1lcmljYVxcL0NoaWNhZ29cIn0iLCJuYmYiOjE3NDcyNDIyMTQuNjIzNjMxLCJleHAiOjE3NDcyNDU4MTQuNTcxNzY5LCJzdWIiOiJzZ2Fnbm9uQHN0Z20ubmV0Iiwic2NvcGVzIjpbIm9wZW5BcGkiXX0.DaDMHQ06q7YTPgSdsJpIimPWsw9d4JWZUHfYx6YLlOfaynyhNZ6tXqA_x8D_JlWo4D8S5QveaUunOzHJsthRKfrYlE1b6vD_nAN9nNSeLtDAbCzXwxItXaNG2uOMmsD-HaUW5yKJm4fOviWr1LR0FmRWCLMtrVhxyk2CQGj1tKVr5FuE1JxfpTOuVeSOjFVC1b1SQKWrk6QU6gG14-w4YB37iX-xHJRzpoVftFYtZODiM15YJR9wPy1yprf1qm9TQtrNJAqW8xIDBdYrBXZTHbvoTlqPJ1u7ica6JABCnQT__fN5x1bLbe9sqct0sNHT3f7UoWkmZoveZ9zYzFLzEw"
                ReviztoAPI.REFRESH_TOKEN = "def50200a5ba8867332c6c09f6a90010d110df68a8e0966d8c7d8386390e34903f1565a985f0229bde9f036428c385670539b429527d0c7a31fb21f7bf397cce88c61acddb7cb31a61eaefb190f21539f9e06f3735833c526084572829fc56252f6df0521654ce7aefd6131c58ad1a422b861a1c91a4e3284b87918bd1c64a6cf908316adad5f86cbc1df867ceec6b5efb48a865f83f8f4e314189299f2554f670ed02bcedc30e0b2bf8ee9a1d3e6d5caa0b4c986d37c87ab8e5256c45fc889847c8466b5b2d51563350207da4a6fb901a4f849e7926466dd7ddab14a03a56aae8db8bd9ea8dcd0ce9d775756569d226b6b3d1a34bf33ee56b61bf5d70032240e58c9002ac38fe60e31acaec643530ad57f225eac489a64a4ef4eccfb8de17515858de84caf89c5f723d167486113d35e9ff6cacb2e74fee87102e0ca6ed0dfd6a8eb36d74f2ef78ed642a0ec0a0e0719ab11cbb59ac609a78d1919ee2a93ab25e1278c55085a4904f531ca31302a62f0c1303c904037f47e8959573c6e50eee2e9fd85d809c0d1d301848e3a34be90760e41be8e02b065f02c1d7442ca22d2861e17d63739ddfcbfdf3ad5c503753f4f7fd17599b423226095d19d2d38d591128ea9b3f9a4c4de13809abbf52147e36f46661254442437085b52208cd8b4b28329671d8f5cae0961f0be4667442b4fd84f59dd166e2cf8c84236d00fe3ed235e3d00d5778742673be31db315d52288e11ca68d0bde61368d189f3a5a57c6ffa91ef6e7b30e8596504525c0f7900761dbd37cc63bdcc3d5c923159fbb32db43ec7b4f7c9556cee5b824f9b4d09896f3de8db25a671b7217c0f524227"
                # Set token expiry to current time + 1 hour
                from datetime import datetime, timedelta
                ReviztoAPI.TOKEN_EXPIRY = datetime.now() + timedelta(seconds=2600)

                print("Revizto API tokens set directly on class")

                # Set the licence UUID
                ReviztoAPI.LICENCE_UUID = licence_uuid
                print(
                    f"Revizto Licence UUID set to: {licence_uuid[:8] if licence_uuid and len(licence_uuid) > 8 else licence_uuid}...")

                # Verify token validity immediately
                if ReviztoAPI.ensure_token_valid():
                    print("Revizto API token verified as valid")
                else:
                    print("WARNING: Revizto API token could not be verified")

                # Try a comprehensive test connection
                print("\n=== RUNNING COMPREHENSIVE CONNECTION TEST ===")
                try:
                    # Test with a direct endpoint first
                    user_licenses_endpoint = "user/licenses"
                    print(f"Testing endpoint: {user_licenses_endpoint}")

                    licenses_response = ReviztoAPI.get(user_licenses_endpoint)
                    if isinstance(licenses_response, dict):
                        print(f"Connection test successful! Response keys: {list(licenses_response.keys())}")
                        print(f"Result code: {licenses_response.get('result')}")
                    else:
                        print(f"Test returned non-dict response: {type(licenses_response)}")

                    print("Revizto API connection test successful")
                except Exception as test_error:
                    print(f"WARNING: Comprehensive connection test failed: {test_error}")
                    import traceback
                    print(f"Test error traceback: {traceback.format_exc()}")

                    # Try a second fallback test with the license endpoint
                    print("\n=== TRYING FALLBACK CONNECTION TEST ===")
                    try:
                        secondary_endpoint = f"license/{licence_uuid}/projects"
                        fallback_response = ReviztoAPI.get(secondary_endpoint)
                        print(f"Fallback test successful! Response type: {type(fallback_response)}")
                    except Exception as fallback_error:
                        print(f"CRITICAL: Fallback test also failed: {fallback_error}")

                # Start the token refresher if enabled
                if getattr(settings, 'REVIZTO_ENABLE_TOKEN_REFRESH', True):
                    token_refresher.initialize(ReviztoAPI)
                    print("Revizto API token refresher started")
                else:
                    print("Revizto API token auto-refresh is disabled")
            else:
                print("CRITICAL: Revizto API tokens not configured in settings")
                if not access_token:
                    print("- Missing REVIZTO_ACCESS_TOKEN")
                if not refresh_token:
                    print("- Missing REVIZTO_REFRESH_TOKEN")
                if not licence_uuid:
                    print("- Missing REVIZTO_LICENCE_UUID")
        except Exception as e:
            import traceback
            print(f"CRITICAL: Error initializing Revizto API client: {e}")
            print(f"Traceback: {traceback.format_exc()}")

        print("====== REVIZTO API INITIALIZATION COMPLETE ======\n")