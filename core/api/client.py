import json
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
        """
        print(f"[DEBUG-INIT] ===== API CLIENT INITIALIZATION =====")
        print(f"[DEBUG-INIT] Access token provided: {'Yes' if access_token else 'No'}")
        print(f"[DEBUG-INIT] Refresh token provided: {'Yes' if refresh_token else 'No'}")

        # Set tokens directly
        cls.ACCESS_TOKEN = access_token
        cls.REFRESH_TOKEN = refresh_token

        # Calculate expiry time (current time + expires_in)
        from datetime import datetime, timedelta
        cls.TOKEN_EXPIRY = datetime.now() + timedelta(seconds=expires_in)
        print(f"[DEBUG-INIT] Token expiry set to: {cls.TOKEN_EXPIRY}")

        # Debug environment
        try:
            print(f"[DEBUG-INIT] Base URL: {cls.BASE_URL}")
            print(f"[DEBUG-INIT] License UUID available: {'Yes' if cls.LICENCE_UUID else 'No'}")
            if cls.LICENCE_UUID:
                preview = cls.LICENCE_UUID[:8] + "..." if len(cls.LICENCE_UUID) > 8 else cls.LICENCE_UUID
                print(f"[DEBUG-INIT] License UUID preview: {preview}")
        except Exception as e:
            print(f"[DEBUG-INIT] Error checking environment: {e}")

        print(f"[DEBUG-INIT] ===== API CLIENT INITIALIZATION COMPLETE =====")
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
            }

            # Add client_id and client_secret if they exist
            client_id = getattr(settings, 'REVIZTO_CLIENT_ID', None)
            client_secret = getattr(settings, 'REVIZTO_CLIENT_SECRET', None)
            if client_id:
                data['client_id'] = client_id
            if client_secret:
                data['client_secret'] = client_secret

            print(f"[DEBUG] Refreshing token with data: {data}")

            response = requests.post(url, headers=headers, data=data)
            print(f"[DEBUG] Token refresh response status: {response.status_code}")

            # Print response content for debugging
            response_text = response.text[:500]  # Limit to first 500 chars
            print(f"[DEBUG] Token refresh response: {response_text}")

            if response.status_code != 200:
                logger.error(f"Token refresh failed with status code: {response.status_code}")
                return False

            # Parse response
            try:
                token_data = response.json()
            except json.JSONDecodeError:
                logger.error("Failed to parse token response as JSON")
                return False

            # Update tokens
            if 'access_token' in token_data:
                cls.ACCESS_TOKEN = token_data['access_token']
                print(f"[DEBUG] Access token updated")
            else:
                logger.error("No access token in refresh response")
                return False

            # Update refresh token if provided
            if 'refresh_token' in token_data:
                cls.REFRESH_TOKEN = token_data['refresh_token']
                print(f"[DEBUG] Refresh token updated")

            # Update token expiry (default: 1 hour)
            expires_in = token_data.get('expires_in', 3600)
            cls.TOKEN_EXPIRY = datetime.now() + timedelta(seconds=expires_in)
            print(f"[DEBUG] Token expiry set to: {cls.TOKEN_EXPIRY}")

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
            print(
                f"[DEBUG] No tokens available. Access token: {'Present' if cls.ACCESS_TOKEN else 'Missing'}, Refresh token: {'Present' if cls.REFRESH_TOKEN else 'Missing'}")
            return False

        # If token expiry is not set, set it to expire soon to force a refresh
        if not cls.TOKEN_EXPIRY:
            print(f"[DEBUG] Token expiry not set, forcing refresh")
            return cls.refresh_token()

        # If token is expired or will expire in next 5 minutes
        if datetime.now() > (cls.TOKEN_EXPIRY - timedelta(minutes=5)):
            print(f"[DEBUG] Token expired or expiring soon, refreshing")
            return cls.refresh_token()

        print(f"[DEBUG] Token valid until {cls.TOKEN_EXPIRY}")
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

    @classmethod
    def test_connection(cls):
        """
        Test the API connection by making a simple request.
        """
        if not cls.ensure_token_valid():
            print("[DEBUG] Failed to obtain valid token for testing")
            return False

        try:
            # Try using a known-working endpoint
            if cls.LICENCE_UUID:
                # Use the license/projects endpoint which we know works
                url = f"https://api.canada.revizto.com/v5/licences"
                response = requests.get(url, headers=cls.get_headers())

                print(f"[DEBUG] Test connection response status: {response.status_code}")
                print(f"[DEBUG] Test response preview: {response.text[:200]}")

                return response.status_code in (200, 404)  # Even a 404 means the API is connected
            else:
                print("[DEBUG] No license UUID configured for test")
                return False
        except Exception as e:
            print(f"[DEBUG] API connection test failed with error: {e}")
            import traceback
            print(f"[DEBUG] API test error traceback: {traceback.format_exc()}")
            return False