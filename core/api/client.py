import logging
import requests
import os
from datetime import datetime, timedelta
from django.conf import settings
from .token_manager import TokenManager

logger = logging.getLogger(__name__)


class ReviztoAPI:
    """
    Client for interacting with the Revizto API.
    Uses TokenManager for token management.
    """
    # Configure with your region from environment or settings
    REGION = os.environ.get('REVIZTO_API_REGION', getattr(settings, 'REVIZTO_API_REGION', 'canada'))
    BASE_URL = f"https://api.{REGION}.revizto.com/v5/"
    LICENCE_UUID = os.environ.get('REVIZTO_LICENCE_UUID', getattr(settings, 'REVIZTO_LICENCE_UUID', None))

    @classmethod
    def initialize(cls, force=False):
        """
        Initialize the API by initializing the TokenManager.
        """
        TokenManager.initialize()
        logger.info("ReviztoAPI client initialized with TokenManager")

    @classmethod
    def get_headers(cls):
        """
        Get headers for API requests, including authorization.

        Returns:
            dict: Headers for API requests
        """
        # Get a fresh access token from TokenManager
        access_token = TokenManager.get_access_token()

        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }


    @classmethod
    def get(cls, endpoint, params=None):
        """
        Make a GET request to the API.

        Args:
            endpoint (str): API endpoint
            params (dict, optional): Query parameters

        Returns:
            dict: Response data

        Raises:
            Exception: If the request fails
        """
        if not cls.ensure_token_valid():
            print(f"[DEBUG] Failed to obtain valid token for endpoint: {endpoint}")
            raise Exception("Failed to obtain valid token")

        url = f"{cls.BASE_URL}{endpoint}"
        print(f"[DEBUG] Making API request to: {url}")
        print(f"[DEBUG] With params: {params}")

        try:
            print(f"[DEBUG] Request headers: {cls.get_headers()}")
            response = requests.get(url, headers=cls.get_headers(), params=params)

            print(f"[DEBUG] Response status code: {response.status_code}")
            print(f"[DEBUG] Response headers: {response.headers}")

            # Print a sample of the response text
            print(f"[DEBUG] Response preview: {response.text[:200]}...")

            # Handle 401 or 403 (token expired or invalid)
            if response.status_code in (401, 403) or "-206" in response.text:
                print(f"[DEBUG] Token expired or invalid. Attempting refresh...")
                # Try to refresh the token and retry the request
                if cls.refresh_token():
                    print(f"[DEBUG] Token refreshed. Retrying request...")
                    # Retry with new token
                    response = requests.get(url, headers=cls.get_headers(), params=params)
                    print(f"[DEBUG] Retry response status: {response.status_code}")
                else:
                    print(f"[DEBUG] Token refresh failed.")
                    raise Exception("Token refresh failed")

            print(f"[DEBUG] Final response status: {response.status_code}")
            response.raise_for_status()
            json_response = response.json()
            print(
                f"[DEBUG] JSON response keys: {list(json_response.keys()) if isinstance(json_response, dict) else 'Not a dict'}")
            return json_response
        except Exception as e:
            import traceback
            print(f"[DEBUG] API GET request failed: {e}")
            print(f"[DEBUG] Error traceback: {traceback.format_exc()}")
            raise

    @classmethod
    def post(cls, endpoint, data=None, json=None):
        """
        Make a POST request to the API.

        Args:
            endpoint (str): API endpoint
            data (dict, optional): Form data
            json (dict, optional): JSON data

        Returns:
            dict: Response data

        Raises:
            Exception: If the request fails
        """
        url = f"{cls.BASE_URL}{endpoint}"
        try:
            response = requests.post(url, headers=cls.get_headers(), data=data, json=json)

            # Handle 401 or 403 (token expired or invalid)
            if response.status_code in (401, 403) or "-206" in response.text:
                # Refresh token and retry
                if TokenManager.refresh_tokens():
                    # Retry with new token
                    response = requests.post(url, headers=cls.get_headers(), data=data, json=json)
                else:
                    raise Exception("Token refresh failed")

            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"API POST request failed: {e}")
            raise

    @classmethod
    def put(cls, endpoint, data=None, json=None):
        """
        Make a PUT request to the API.

        Args:
            endpoint (str): API endpoint
            data (dict, optional): Form data
            json (dict, optional): JSON data

        Returns:
            dict: Response data

        Raises:
            Exception: If the request fails
        """
        url = f"{cls.BASE_URL}{endpoint}"
        try:
            response = requests.put(url, headers=cls.get_headers(), data=data, json=json)

            # Handle 401 or 403 (token expired or invalid)
            if response.status_code in (401, 403) or "-206" in response.text:
                # Refresh token and retry
                if TokenManager.refresh_tokens():
                    # Retry with new token
                    response = requests.put(url, headers=cls.get_headers(), data=data, json=json)
                else:
                    raise Exception("Token refresh failed")

            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"API PUT request failed: {e}")
            raise

    @classmethod
    def delete(cls, endpoint):
        """
        Make a DELETE request to the API.

        Args:
            endpoint (str): API endpoint

        Returns:
            bool: True if successful, False otherwise

        Raises:
            Exception: If the request fails
        """
        url = f"{cls.BASE_URL}{endpoint}"
        try:
            response = requests.delete(url, headers=cls.get_headers())

            # Handle 401 or 403 (token expired or invalid)
            if response.status_code in (401, 403) or "-206" in response.text:
                # Refresh token and retry
                if TokenManager.refresh_tokens():
                    # Retry with new token
                    response = requests.delete(url, headers=cls.get_headers())
                else:
                    raise Exception("Token refresh failed")

            response.raise_for_status()
            return response.status_code == 204
        except Exception as e:
            logger.error(f"API DELETE request failed: {e}")
            raise