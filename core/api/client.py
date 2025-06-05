# core/api/client.py - Key improvements to add to your existing client

import json
import logging
import requests
from datetime import datetime, timedelta, time
from django.conf import settings
from django.utils import timezone
from . import token_store

logger = logging.getLogger(__name__)


class ReviztoAPI:
    """
    Enhanced client for interacting with the Revizto API.
    Handles token refresh and API requests with improved error handling.
    """
    REGION = "canada"
    BASE_URL = f"https://api.{REGION}.revizto.com/v5/"

    @classmethod
    def initialize(cls, access_token, refresh_token, licence_uuid, expires_in=3600):
        """Initialize the API with tokens and store them persistently."""
        logger.info("Initializing ReviztoAPI with persistent token storage")

        # Store tokens in database
        success = token_store.set_tokens(
            access_token,
            refresh_token,
            licence_uuid,
            expires_in=expires_in
        )

        if success:
            logger.info("API client initialized successfully with persistent storage")
        else:
            logger.error("Failed to initialize API client - token storage failed")

        return success

    @classmethod
    def refresh_token(cls):
        """Refresh the access token using the refresh token."""
        refresh_token = token_store.get_refresh_token()
        if not refresh_token:
            logger.error("No refresh token available for refresh")
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

            logger.info("Attempting token refresh...")
            response = requests.post(url, headers=headers, data=data, timeout=30)

            if response.status_code != 200:
                logger.error(f"Token refresh failed with status {response.status_code}: {response.text[:500]}")
                return False

            try:
                token_data = response.json()
            except json.JSONDecodeError:
                logger.error("Failed to parse token response as JSON")
                return False

            # Extract new tokens
            new_access_token = token_data.get('access_token')
            new_refresh_token = token_data.get('refresh_token')
            expires_in = token_data.get('expires_in', 3600)

            if not new_access_token:
                logger.error("No access token in refresh response")
                return False

            # Update stored tokens
            current_licence_uuid = token_store.get_licence_uuid()
            success = token_store.set_tokens(
                new_access_token,
                new_refresh_token or refresh_token,  # Use new refresh token if provided
                current_licence_uuid,
                expires_in=expires_in
            )

            if success:
                logger.info("Successfully refreshed and stored access token")
                return True
            else:
                logger.error("Failed to store refreshed tokens")
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during token refresh: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during token refresh: {e}")
            return False

    @classmethod
    def ensure_token_valid(cls):
        """Ensure the access token is valid, refresh if needed."""
        # Check if we have tokens
        if not token_store.has_tokens():
            logger.warning("No tokens available, attempting re-initialization from settings")
            return cls._attempt_reinitialize_from_settings()

        # Check if token is expired
        if token_store.is_token_expired():
            logger.info("Token expired, attempting refresh")
            return cls.refresh_token()

        logger.debug("Token is valid")
        return True

    @classmethod
    def _attempt_reinitialize_from_settings(cls):
        """Attempt to reinitialize tokens from Django settings."""
        try:
            access_token = getattr(settings, 'REVIZTO_ACCESS_TOKEN', '')
            refresh_token = getattr(settings, 'REVIZTO_REFRESH_TOKEN', '')
            licence_uuid = getattr(settings, 'REVIZTO_LICENCE_UUID', '')

            if all([access_token, refresh_token, licence_uuid]):
                logger.info("Reinitializing tokens from settings")
                return cls.initialize(access_token, refresh_token, licence_uuid)
            else:
                logger.error("Cannot reinitialize - missing tokens in settings")
                return False
        except Exception as e:
            logger.error(f"Error reinitializing from settings: {e}")
            return False

    @classmethod
    def get_headers(cls):
        """Get headers for API requests, including authorization."""
        access_token = token_store.get_access_token()
        if not access_token:
            raise Exception("No access token available")

        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @classmethod
    def get_licence_uuid(cls):
        """Get the license UUID from token store or settings."""
        licence_uuid = token_store.get_licence_uuid()
        if licence_uuid:
            return licence_uuid

        # Fallback to settings
        return getattr(settings, 'REVIZTO_LICENCE_UUID', '')

    @classmethod
    def get(cls, endpoint, params=None, max_retries=3):
        """Make a GET request to the API with improved error handling."""
        last_exception = None

        for attempt in range(max_retries):
            try:
                # Ensure we have a valid token
                if not cls.ensure_token_valid():
                    raise Exception("Failed to obtain valid token")

                url = f"{cls.BASE_URL}{endpoint}"
                logger.debug(f"Making API request to: {url} (attempt {attempt + 1})")

                response = requests.get(
                    url,
                    headers=cls.get_headers(),
                    params=params,
                    timeout=60  # 60 second timeout
                )

                # Handle token expiry responses
                if response.status_code in (401, 403):
                    logger.warning(f"Received {response.status_code}, token may be expired")
                    if cls.refresh_token():
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
                return response.json()

            except requests.exceptions.Timeout as e:
                last_exception = e
                logger.warning(f"Request timeout on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue

            except requests.exceptions.ConnectionError as e:
                last_exception = e
                logger.warning(f"Connection error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue

            except requests.exceptions.RequestException as e:
                last_exception = e
                logger.error(f"Request error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue

            except Exception as e:
                last_exception = e
                logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue

        # If we get here, all retries failed
        raise Exception(f"API request failed after {max_retries} attempts. Last error: {last_exception}")

    @classmethod
    def test_connection(cls):
        """Test the API connection."""
        try:
            if not cls.ensure_token_valid():
                logger.error("Cannot test connection - no valid token")
                return False

            # Try a simple API call
            licence_uuid = cls.get_licence_uuid()
            if licence_uuid:
                response = requests.get(
                    f"{cls.BASE_URL}licences",
                    headers=cls.get_headers(),
                    timeout=30
                )

                success = response.status_code in (200, 404)  # 404 is also OK for testing
                logger.info(f"Connection test result: {success} (status: {response.status_code})")
                return success
            else:
                logger.error("No license UUID available for connection test")
                return False

        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False