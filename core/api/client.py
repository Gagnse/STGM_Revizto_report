import logging
import requests
from datetime import datetime, timedelta
from django.conf import settings

logger = logging.getLogger(__name__)


class ReviztoAPI:
    """
    Client for interacting with the Revizto API.
    Handles token refresh and API requests.
    """
    # Configure with your region
    REGION = "canada"
    BASE_URL = f"https://api.{REGION}.revizto.com/v5/"
    LICENCE_UUID = settings.REVIZTO_LICENCE_UUID
    # Store tokens as class variables
    ACCESS_TOKEN = None
    REFRESH_TOKEN = None
    TOKEN_EXPIRY = None

    @classmethod
    def initialize(cls, access_token, refresh_token, expires_in=3600):
        """
        Initialize the API with tokens.

        Args:
            access_token (str): The access token
            refresh_token (str): The refresh token
            expires_in (int): Token expiration time in seconds (default: 1 hour)
        """
        cls.ACCESS_TOKEN = access_token
        cls.REFRESH_TOKEN = refresh_token
        # Calculate expiry time (current time + expires_in)
        cls.TOKEN_EXPIRY = datetime.now() + timedelta(seconds=expires_in)
        logger.info("API client initialized with tokens")

    @classmethod
    def refresh_token(cls):
        """
        Refresh the access token using the refresh token.

        Returns:
            bool: True if successful, False otherwise
        """
        if not cls.REFRESH_TOKEN:
            logger.error("No refresh token available")
            return False

        try:
            # Prepare the refresh token request as per Revizto API documentation
            url = f"{cls.BASE_URL}oauth2"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            # Format the data exactly as required by the Revizto API
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': cls.REFRESH_TOKEN,
                'client_id': getattr(settings, 'REVIZTO_CLIENT_ID', None),  # Add if required
                'client_secret': getattr(settings, 'REVIZTO_CLIENT_SECRET', None)  # Add if required
            }

            # Remove any None values from the data
            data = {k: v for k, v in data.items() if v is not None}

            print(f"[DEBUG] Refreshing token with data: {data}")

            response = requests.post(url, headers=headers, data=data)
            print(f"[DEBUG] Token refresh response status: {response.status_code}")
            print(f"[DEBUG] Token refresh response headers: {response.headers}")

            # Print response content for debugging
            response_text = response.text[:500]  # Limit to first 500 chars
            print(f"[DEBUG] Token refresh response: {response_text}")

            response.raise_for_status()

            # Parse response
            token_data = response.json()

            # Update tokens
            if 'access_token' in token_data:
                cls.ACCESS_TOKEN = token_data['access_token']
            else:
                logger.error("No access token in refresh response")
                return False

            # Update refresh token if provided
            if 'refresh_token' in token_data:
                cls.REFRESH_TOKEN = token_data['refresh_token']

            # Update token expiry (default: 1 hour)
            expires_in = token_data.get('expires_in', 3600)
            cls.TOKEN_EXPIRY = datetime.now() + timedelta(seconds=expires_in)

            logger.info("Successfully refreshed access token")
            return True
        except Exception as e:
            logger.error(f"Failed to refresh token: {e}")
            return False

    @classmethod
    def ensure_token_valid(cls):
        """
        Ensure the access token is valid, refresh if needed.

        Returns:
            bool: True if a valid token is available, False otherwise
        """
        if not cls.ACCESS_TOKEN or not cls.REFRESH_TOKEN:
            logger.error("No tokens available")
            return False

        # If token is expired or will expire in next 5 minutes
        if not cls.TOKEN_EXPIRY or datetime.now() > (cls.TOKEN_EXPIRY - timedelta(minutes=5)):
            return cls.refresh_token()

        return True

    @classmethod
    def get_headers(cls):
        """
        Get headers for API requests, including authorization.

        Returns:
            dict: Headers for API requests
        """
        return {
            "Authorization": f"Bearer {cls.ACCESS_TOKEN}",
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

            # Print a sample of the response text
            response_preview = response.text[:200] if response.text else "Empty response"
            print(f"[DEBUG] Response preview: {response_preview}...")

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

            if isinstance(json_response, dict):
                print(f"[DEBUG] JSON response keys: {list(json_response.keys())}")
            else:
                print(f"[DEBUG] JSON response type: {type(json_response)}")

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
        if not cls.ensure_token_valid():
            raise Exception("Failed to obtain valid token")

        url = f"{cls.BASE_URL}{endpoint}"
        try:
            response = requests.post(url, headers=cls.get_headers(), data=data, json=json)

            # Handle 401 or 403 (token expired or invalid)
            if response.status_code in (401, 403) or "-206" in response.text:
                # Try to refresh the token and retry the request
                if cls.refresh_token():
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
        if not cls.ensure_token_valid():
            raise Exception("Failed to obtain valid token")

        url = f"{cls.BASE_URL}{endpoint}"
        try:
            response = requests.put(url, headers=cls.get_headers(), data=data, json=json)

            # Handle 401 or 403 (token expired or invalid)
            if response.status_code in (401, 403) or "-206" in response.text:
                # Try to refresh the token and retry the request
                if cls.refresh_token():
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
        if not cls.ensure_token_valid():
            raise Exception("Failed to obtain valid token")

        url = f"{cls.BASE_URL}{endpoint}"
        try:
            response = requests.delete(url, headers=cls.get_headers())

            # Handle 401 or 403 (token expired or invalid)
            if response.status_code in (401, 403) or "-206" in response.text:
                # Try to refresh the token and retry the request
                if cls.refresh_token():
                    # Retry with new token
                    response = requests.delete(url, headers=cls.get_headers())
                else:
                    raise Exception("Token refresh failed")

            response.raise_for_status()
            return response.status_code == 204
        except Exception as e:
            logger.error(f"API DELETE request failed: {e}")
            raise