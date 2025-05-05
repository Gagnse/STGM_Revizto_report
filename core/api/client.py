import requests
import logging
from datetime import datetime, timedelta
from django.conf import settings

logger = logging.getLogger(__name__)


class ReviztoAPI:
    """
    Simple client for interacting with the Revizto API.
    Handles token refresh and API requests.
    """
    BASE_URL = "https://api.canada.revizto.com/v5/"

    # Store tokens as class variables for simplicity
    # In a real application, consider more secure storage
    ACCESS_TOKEN = None
    REFRESH_TOKEN = None
    TOKEN_EXPIRY = None

    @classmethod
    def initialize(cls, access_token, refresh_token):
        """Initialize the API with tokens."""
        cls.ACCESS_TOKEN = access_token
        cls.REFRESH_TOKEN = refresh_token
        # Set a default expiry time (e.g., 1 hour from now)
        cls.TOKEN_EXPIRY = datetime.now() + timedelta(hours=1)

    @classmethod
    def refresh_token(cls):
        """Refresh the access token using the refresh token."""
        if not cls.REFRESH_TOKEN:
            logger.error("No refresh token available")
            return False

        try:
            response = requests.post(
                f"{cls.BASE_URL}auth/refresh",
                json={"refresh_token": cls.REFRESH_TOKEN}
            )
            response.raise_for_status()

            data = response.json()
            cls.ACCESS_TOKEN = data.get("access_token")
            # Update refresh token if a new one is provided
            if data.get("refresh_token"):
                cls.REFRESH_TOKEN = data.get("refresh_token")

            # Update token expiry
            expires_in = data.get("expires_in", 3600)  # Default to 1 hour
            cls.TOKEN_EXPIRY = datetime.now() + timedelta(seconds=expires_in)

            logger.info("Successfully refreshed access token")
            return True
        except Exception as e:
            logger.error(f"Failed to refresh token: {e}")
            return False

    @classmethod
    def ensure_token_valid(cls):
        """Ensure the access token is valid, refresh if needed."""
        if not cls.ACCESS_TOKEN or not cls.REFRESH_TOKEN:
            logger.error("No tokens available")
            return False

        # If token is expired or will expire in next 5 minutes
        if not cls.TOKEN_EXPIRY or datetime.now() > (cls.TOKEN_EXPIRY - timedelta(minutes=5)):
            return cls.refresh_token()

        return True

    @classmethod
    def get_headers(cls):
        """Get headers for API requests, including authorization."""
        return {
            "Authorization": f"Bearer {cls.ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @classmethod
    def get(cls, endpoint, params=None):
        """Make a GET request to the API."""
        if not cls.ensure_token_valid():
            raise Exception("Failed to obtain valid token")

        url = f"{cls.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, headers=cls.get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"API GET request failed: {e}")
            raise

    @classmethod
    def post(cls, endpoint, data=None, json=None):
        """Make a POST request to the API."""
        if not cls.ensure_token_valid():
            raise Exception("Failed to obtain valid token")

        url = f"{cls.BASE_URL}{endpoint}"
        try:
            response = requests.post(url, headers=cls.get_headers(), data=data, json=json)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"API POST request failed: {e}")
            raise

    @classmethod
    def put(cls, endpoint, data=None, json=None):
        """Make a PUT request to the API."""
        if not cls.ensure_token_valid():
            raise Exception("Failed to obtain valid token")

        url = f"{cls.BASE_URL}{endpoint}"
        try:
            response = requests.put(url, headers=cls.get_headers(), data=data, json=json)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"API PUT request failed: {e}")
            raise

    @classmethod
    def delete(cls, endpoint):
        """Make a DELETE request to the API."""
        if not cls.ensure_token_valid():
            raise Exception("Failed to obtain valid token")

        url = f"{cls.BASE_URL}{endpoint}"
        try:
            response = requests.delete(url, headers=cls.get_headers())
            response.raise_for_status()
            return response.status_code == 204
        except Exception as e:
            logger.error(f"API DELETE request failed: {e}")
            raise