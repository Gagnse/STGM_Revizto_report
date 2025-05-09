import os
import logging
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
from django.conf import settings
from django.utils.timezone import make_aware

logger = logging.getLogger(__name__)


class TokenManager:
    """
    Manages Revizto API tokens, including storage, automatic refresh, and persistence.
    """
    # Token state
    _access_token = None
    _refresh_token = None
    _token_expiry = None
    _initialized = False
    _refresh_in_progress = False

    # Path to token file
    TOKEN_FILE = Path(settings.BASE_DIR) / '.revizto_tokens.json'

    @classmethod
    def initialize(cls):
        """
        Initialize the token manager with tokens from file, environment variables, or settings.
        """
        if cls._initialized:
            return

        logger.info("Initializing TokenManager")

        # Try to load tokens from file first
        file_tokens = cls._load_tokens_from_file()
        if file_tokens:
            cls._access_token = file_tokens.get('access_token')
            cls._refresh_token = file_tokens.get('refresh_token')

            # Convert expiry string to datetime if present
            expiry_str = file_tokens.get('token_expiry')
            if expiry_str:
                try:
                    cls._token_expiry = datetime.fromisoformat(expiry_str)
                    logger.info(f"Loaded tokens from file, valid until: {cls._token_expiry}")
                except (ValueError, TypeError):
                    # If we can't parse the expiry, set a conservative one
                    cls._token_expiry = datetime.now() + timedelta(minutes=30)
            else:
                cls._token_expiry = datetime.now() + timedelta(minutes=30)

            cls._initialized = True
            logger.info("TokenManager initialized with tokens from file")
            return

        # If file loading failed, try environment variables
        access_token = os.environ.get('REVIZTO_ACCESS_TOKEN')
        refresh_token = os.environ.get('REVIZTO_REFRESH_TOKEN')

        # Fall back to Django settings if environment variables are not set
        if not access_token or not refresh_token:
            access_token = getattr(settings, 'REVIZTO_ACCESS_TOKEN', None)
            refresh_token = getattr(settings, 'REVIZTO_REFRESH_TOKEN', None)

        if access_token and refresh_token:
            cls._access_token = access_token
            cls._refresh_token = refresh_token
            # Set initial expiry (conservatively 30 minutes from now)
            cls._token_expiry = datetime.now() + timedelta(minutes=30)
            cls._initialized = True

            # Save tokens to file
            cls._save_tokens_to_file()

            logger.info("TokenManager initialized with tokens from env/settings")
        else:
            logger.error("TokenManager initialization failed: No tokens available")
            raise Exception(
                "No Revizto API tokens available. Please set REVIZTO_ACCESS_TOKEN and REVIZTO_REFRESH_TOKEN.")

    @classmethod
    def get_access_token(cls):
        """
        Get the current access token, refreshing if necessary.

        Returns:
            str: The current valid access token
        """
        if not cls._initialized:
            cls.initialize()

        # Check if token is expired or will expire in next 5 minutes
        if cls._token_expiry and datetime.now() > (cls._token_expiry - timedelta(minutes=5)):
            logger.info("Access token is expired or will expire soon, refreshing")
            cls.refresh_tokens()

        return cls._access_token

    @classmethod
    def get_refresh_token(cls):
        """
        Get the current refresh token.

        Returns:
            str: The current refresh token
        """
        if not cls._initialized:
            cls.initialize()

        return cls._refresh_token

    @classmethod
    def refresh_tokens(cls):
        """
        Refresh the tokens using the refresh token.

        Returns:
            bool: True if successful, False otherwise
        """
        if cls._refresh_in_progress:
            logger.info("Token refresh already in progress, waiting...")
            return False

        cls._refresh_in_progress = True

        try:
            logger.info("Refreshing Revizto API tokens")

            if not cls._refresh_token:
                logger.error("Cannot refresh tokens: No refresh token available")
                cls._refresh_in_progress = False
                return False

            # Get the API region
            region = os.environ.get('REVIZTO_API_REGION', getattr(settings, 'REVIZTO_API_REGION', 'canada'))

            # Prepare the refresh token request
            url = f"https://api.{region}.revizto.com/v5/oauth2"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': cls._refresh_token
            }

            # Make the request
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()

            # Parse response
            token_data = response.json()
            logger.debug(f"Token refresh response keys: {list(token_data.keys())}")

            # Update tokens
            if 'access_token' in token_data:
                cls._access_token = token_data['access_token']
                # Update environment variable for persistence
                os.environ['REVIZTO_ACCESS_TOKEN'] = cls._access_token
                logger.info("Access token refreshed and updated in environment")
            else:
                logger.error("No access token in refresh response")
                cls._refresh_in_progress = False
                return False

            # Update refresh token if provided
            if 'refresh_token' in token_data:
                cls._refresh_token = token_data['refresh_token']
                # Update environment variable for persistence
                os.environ['REVIZTO_REFRESH_TOKEN'] = cls._refresh_token
                logger.info("Refresh token updated in environment")

            # Update token expiry
            expires_in = token_data.get('expires_in', 3600)  # Default 1 hour
            cls._token_expiry = datetime.now() + timedelta(seconds=expires_in)

            # Save updated tokens to file
            cls._save_tokens_to_file()

            logger.info(f"Successfully refreshed tokens, valid until: {cls._token_expiry}")
            cls._refresh_in_progress = False
            return True

        except Exception as e:
            logger.error(f"Failed to refresh tokens: {e}")
            cls._refresh_in_progress = False
            return False

    @classmethod
    def _save_tokens_to_file(cls):
        """
        Save tokens to a local file for persistence.
        """
        try:
            token_data = {
                'access_token': cls._access_token,
                'refresh_token': cls._refresh_token,
                'token_expiry': cls._token_expiry.isoformat() if cls._token_expiry else None,
                'updated_at': datetime.now().isoformat()
            }

            # Create the file with restricted permissions
            with open(cls.TOKEN_FILE, 'w') as f:
                json.dump(token_data, f)

            # Set file permissions to be readable only by the owner
            os.chmod(cls.TOKEN_FILE, 0o600)

            logger.info(f"Tokens saved to file: {cls.TOKEN_FILE}")
            return True
        except Exception as e:
            logger.error(f"Failed to save tokens to file: {e}")
            return False

    @classmethod
    def _load_tokens_from_file(cls):
        """
        Load tokens from local file.

        Returns:
            dict: Token data if available, None otherwise
        """
        try:
            if not cls.TOKEN_FILE.exists():
                logger.info(f"Token file not found: {cls.TOKEN_FILE}")
                return None

            with open(cls.TOKEN_FILE, 'r') as f:
                token_data = json.load(f)

            logger.info(f"Tokens loaded from file: {cls.TOKEN_FILE}")
            return token_data
        except Exception as e:
            logger.error(f"Failed to load tokens from file: {e}")
            return None

    @classmethod
    def is_valid(cls):
        """
        Check if the current tokens are valid.

        Returns:
            bool: True if valid tokens are available, False otherwise
        """
        if not cls._initialized:
            try:
                cls.initialize()
            except Exception as e:
                logger.error(f"Failed to initialize token manager: {e}")
                return False

        return bool(cls._access_token and cls._refresh_token)