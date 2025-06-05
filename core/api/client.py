# core/api/client.py - Fixed version with proper PostgreSQL token storage

import json
import logging
import requests
from datetime import datetime, timedelta
import time
from django.conf import settings
from django.utils import timezone
from . import token_store

logger = logging.getLogger(__name__)


class ReviztoAPI:
    """
    Enhanced client for interacting with the Revizto API.
    Handles token refresh and API requests with PostgreSQL token storage.
    """
    REGION = "canada"
    BASE_URL = f"https://api.{REGION}.revizto.com/v5/"

    @classmethod
    def initialize(cls, access_token, refresh_token, licence_uuid, expires_in=3600):
        """Initialize the API with tokens and store them in PostgreSQL database."""
        print(f"[REVIZTO-API] Initializing API with PostgreSQL token storage")
        print(f"[REVIZTO-API] Access token: {len(access_token)} chars")
        print(f"[REVIZTO-API] Refresh token: {len(refresh_token)} chars")
        print(f"[REVIZTO-API] License UUID: {licence_uuid}")

        # Store tokens in PostgreSQL database
        success = token_store.set_tokens(
            access_token,
            refresh_token,
            licence_uuid,
            expires_in=expires_in
        )

        if success:
            print(f"[REVIZTO-API] ✅ API client initialized successfully with PostgreSQL storage")

            # Verify storage by reading back
            stored_access = token_store.get_access_token()
            stored_refresh = token_store.get_refresh_token()
            stored_uuid = token_store.get_licence_uuid()

            if stored_access and stored_refresh and stored_uuid:
                print(f"[REVIZTO-API] ✅ Token storage verification successful")
                return True
            else:
                print(f"[REVIZTO-API] ❌ Token storage verification failed")
                return False
        else:
            print(f"[REVIZTO-API] ❌ Failed to initialize API client - PostgreSQL storage failed")
            return False

    @classmethod
    def refresh_token(cls):
        """Refresh the access token using the refresh token from PostgreSQL."""
        print(f"[REVIZTO-API] Starting token refresh process...")

        refresh_token = token_store.get_refresh_token()
        if not refresh_token:
            print(f"[REVIZTO-API] ❌ No refresh token available in PostgreSQL")
            return False

        try:
            url = f"{cls.BASE_URL}oauth2"
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}

            data = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
            }

            # Add client credentials if available
            client_id = getattr(settings, 'REVIZTO_CLIENT_ID', None)
            client_secret = getattr(settings, 'REVIZTO_CLIENT_SECRET', None)
            if client_id:
                data['client_id'] = client_id
            if client_secret:
                data['client_secret'] = client_secret

            print(f"[REVIZTO-API] Sending refresh request to: {url}")
            response = requests.post(url, headers=headers, data=data, timeout=30)

            if response.status_code != 200:
                print(f"[REVIZTO-API] ❌ Token refresh failed with status {response.status_code}")
                print(f"[REVIZTO-API] Response: {response.text[:500]}")
                token_store.record_refresh_attempt(success=False)
                return False

            try:
                token_data = response.json()
            except json.JSONDecodeError:
                print(f"[REVIZTO-API] ❌ Failed to parse token response as JSON")
                token_store.record_refresh_attempt(success=False)
                return False

            # Extract new tokens
            new_access_token = token_data.get('access_token')
            new_refresh_token = token_data.get('refresh_token')
            expires_in = token_data.get('expires_in', 3600)

            if not new_access_token:
                print(f"[REVIZTO-API] ❌ No access token in refresh response")
                token_store.record_refresh_attempt(success=False)
                return False

            print(f"[REVIZTO-API] ✅ Received new tokens from API")
            print(f"[REVIZTO-API] New access token: {len(new_access_token)} chars")
            print(f"[REVIZTO-API] New refresh token: {len(new_refresh_token) if new_refresh_token else 'None'} chars")
            print(f"[REVIZTO-API] Expires in: {expires_in} seconds")

            # Update stored tokens in PostgreSQL
            current_licence_uuid = token_store.get_licence_uuid()
            success = token_store.set_tokens(
                new_access_token,
                new_refresh_token or refresh_token,  # Use new refresh token if provided
                current_licence_uuid,
                expires_in=expires_in
            )

            if success:
                print(f"[REVIZTO-API] ✅ Successfully refreshed and stored tokens in PostgreSQL")
                token_store.record_refresh_attempt(success=True)
                return True
            else:
                print(f"[REVIZTO-API] ❌ Failed to store refreshed tokens in PostgreSQL")
                token_store.record_refresh_attempt(success=False)
                return False

        except requests.exceptions.RequestException as e:
            print(f"[REVIZTO-API] ❌ Network error during token refresh: {e}")
            token_store.record_refresh_attempt(success=False)
            return False
        except Exception as e:
            print(f"[REVIZTO-API] ❌ Unexpected error during token refresh: {e}")
            token_store.record_refresh_attempt(success=False)
            return False

    @classmethod
    def ensure_token_valid(cls):
        """Ensure the access token is valid, refresh if needed."""
        print(f"[REVIZTO-API] Checking token validity...")

        # Check if we have tokens in PostgreSQL
        if not token_store.has_tokens():
            print(f"[REVIZTO-API] ⚠️ No tokens available in PostgreSQL, attempting re-initialization from settings")
            return cls._attempt_reinitialize_from_settings()

        # Check if token is expired
        if token_store.is_token_expired():
            print(f"[REVIZTO-API] 🔄 Token expired, attempting refresh")
            return cls.refresh_token()

        print(f"[REVIZTO-API] ✅ Token is valid")
        return True

    @classmethod
    def _attempt_reinitialize_from_settings(cls):
        """Attempt to reinitialize tokens from Django settings."""
        try:
            print(f"[REVIZTO-API] Attempting to reinitialize from Django settings...")

            access_token = getattr(settings, 'REVIZTO_ACCESS_TOKEN', '')
            refresh_token = getattr(settings, 'REVIZTO_REFRESH_TOKEN', '')
            licence_uuid = getattr(settings, 'REVIZTO_LICENCE_UUID', '')

            if all([access_token, refresh_token, licence_uuid]):
                print(f"[REVIZTO-API] 🔄 Reinitializing tokens from settings")
                return cls.initialize(access_token, refresh_token, licence_uuid)
            else:
                print(f"[REVIZTO-API] ❌ Cannot reinitialize - missing tokens in settings")
                print(f"[REVIZTO-API] Access: {'✅' if access_token else '❌'}")
                print(f"[REVIZTO-API] Refresh: {'✅' if refresh_token else '❌'}")
                print(f"[REVIZTO-API] License: {'✅' if licence_uuid else '❌'}")
                return False
        except Exception as e:
            print(f"[REVIZTO-API] ❌ Error reinitializing from settings: {e}")
            return False

    @classmethod
    def get_headers(cls):
        """Get headers for API requests, including authorization."""
        access_token = token_store.get_access_token()
        if not access_token:
            raise Exception("No access token available in PostgreSQL storage")

        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @classmethod
    def get_licence_uuid(cls):
        """Get the license UUID from PostgreSQL storage or settings."""
        licence_uuid = token_store.get_licence_uuid()
        if licence_uuid:
            return licence_uuid

        # Fallback to settings
        fallback_uuid = getattr(settings, 'REVIZTO_LICENCE_UUID', '')
        if fallback_uuid:
            print(f"[REVIZTO-API] Using fallback license UUID from settings")
        return fallback_uuid

    @classmethod
    def get(cls, endpoint, params=None, max_retries=3):
        """Make a GET request to the API with improved error handling."""
        last_exception = None

        for attempt in range(max_retries):
            try:
                print(f"[REVIZTO-API] Making API request (attempt {attempt + 1}/{max_retries})")

                # Ensure we have a valid token
                if not cls.ensure_token_valid():
                    raise Exception("Failed to obtain valid token from PostgreSQL storage")

                url = f"{cls.BASE_URL}{endpoint}"
                print(f"[REVIZTO-API] Request URL: {url}")

                response = requests.get(
                    url,
                    headers=cls.get_headers(),
                    params=params,
                    timeout=60  # 60 second timeout
                )

                # Handle token expiry responses
                if response.status_code in (401, 403):
                    print(f"[REVIZTO-API] ⚠️ Received {response.status_code}, token may be expired")
                    if cls.refresh_token():
                        print(f"[REVIZTO-API] 🔄 Token refreshed, retrying request")
                        # Retry with new token
                        response = requests.get(
                            url,
                            headers=cls.get_headers(),
                            params=params,
                            timeout=60
                        )
                    else:
                        raise Exception("Token refresh failed after 401/403")

                response.raise_for_status()
                print(f"[REVIZTO-API] ✅ API request successful (status: {response.status_code})")
                return response.json()

            except requests.exceptions.Timeout as e:
                last_exception = e
                print(f"[REVIZTO-API] ⚠️ Request timeout on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"[REVIZTO-API] Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    continue

            except requests.exceptions.ConnectionError as e:
                last_exception = e
                print(f"[REVIZTO-API] ⚠️ Connection error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"[REVIZTO-API] Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    continue

            except requests.exceptions.RequestException as e:
                last_exception = e
                print(f"[REVIZTO-API] ❌ Request error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"[REVIZTO-API] Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    continue

            except Exception as e:
                last_exception = e
                print(f"[REVIZTO-API] ❌ Unexpected error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"[REVIZTO-API] Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    continue

        # If we get here, all retries failed
        error_msg = f"API request failed after {max_retries} attempts. Last error: {last_exception}"
        print(f"[REVIZTO-API] ❌ {error_msg}")
        raise Exception(error_msg)

    @classmethod
    def test_connection(cls):
        """Test the API connection using tokens from PostgreSQL."""
        try:
            print(f"[REVIZTO-API] Testing API connection...")

            if not cls.ensure_token_valid():
                print(f"[REVIZTO-API] ❌ Cannot test connection - no valid token in PostgreSQL")
                return False

            # Try a simple API call
            licence_uuid = cls.get_licence_uuid()
            if licence_uuid:
                print(f"[REVIZTO-API] Testing with license UUID: {licence_uuid}")
                response = requests.get(
                    f"{cls.BASE_URL}licences",
                    headers=cls.get_headers(),
                    timeout=30
                )

                success = response.status_code in (200, 404)  # 404 is also OK for testing
                print(
                    f"[REVIZTO-API] Connection test result: {'✅ Success' if success else '❌ Failed'} (status: {response.status_code})")
                return success
            else:
                print(f"[REVIZTO-API] ❌ No license UUID available for connection test")
                return False

        except Exception as e:
            print(f"[REVIZTO-API] ❌ Connection test failed: {e}")
            return False

    @classmethod
    def get_token_debug_info(cls):
        """Get debug information about current token state"""
        try:
            status = token_store.get_token_status()
            print(f"[REVIZTO-API] 📊 TOKEN DEBUG INFO:")
            print(f"[REVIZTO-API] PostgreSQL connection: {'✅' if 'error' not in status else '❌'}")
            if 'error' not in status:
                print(
                    f"[REVIZTO-API] Access token: {'✅' if status['has_access_token'] else '❌'} ({status.get('access_token_length', 0)} chars)")
                print(
                    f"[REVIZTO-API] Refresh token: {'✅' if status['has_refresh_token'] else '❌'} ({status.get('refresh_token_length', 0)} chars)")
                print(f"[REVIZTO-API] License UUID: {'✅' if status['has_licence_uuid'] else '❌'}")
                print(f"[REVIZTO-API] Token expired: {'🔴 Yes' if status['is_expired'] else '🟢 No'}")
                print(f"[REVIZTO-API] Last refresh: {status['last_successful_refresh'] or 'Never'}")
            else:
                print(f"[REVIZTO-API] Error: {status['error']}")
            return status
        except Exception as e:
            print(f"[REVIZTO-API] ❌ Error getting debug info: {e}")
            return {"error": str(e)}