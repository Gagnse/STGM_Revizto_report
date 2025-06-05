# core/api/token_refresher.py - Replace your existing file

"""
Enhanced token refresh module for Revizto API.
Designed to work reliably on Heroku with automatic recovery.
"""

import threading
import time
import logging
import os
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings

logger = logging.getLogger(__name__)

class HerokuTokenRefresher:
    """
    Enhanced token refresher designed for Heroku environment.
    Handles dyno restarts and connection issues gracefully.
    """

    def __init__(self, api_client, refresh_interval=1800):  # 30 minutes
        """
        Initialize the token refresher.

        Args:
            api_client: The ReviztoAPI client class
            refresh_interval: Refresh interval in seconds (default: 30 minutes)
        """
        self.api_client = api_client
        self.refresh_interval = refresh_interval
        self.refresh_thread = None
        self.stop_event = threading.Event()
        self.last_refresh_time = None
        self.consecutive_failures = 0
        self.max_failures = 5  # Maximum consecutive failures before backing off

        # Heroku-specific settings
        self.is_heroku = bool(os.environ.get('DYNO'))
        self.heroku_dyno_id = os.environ.get('DYNO', 'local')

        logger.info(f"TokenRefresher initialized on {'Heroku' if self.is_heroku else 'local'} environment")

    def start(self):
        """Start the token refresh thread if not already running."""
        if self.refresh_thread is None or not self.refresh_thread.is_alive():
            logger.info(f"Starting token refresh thread on {self.heroku_dyno_id}")
            self.stop_event.clear()
            self.refresh_thread = threading.Thread(target=self._refresh_loop, daemon=True)
            self.refresh_thread.start()
            return True
        else:
            logger.info("Token refresh thread is already running")
            return False

    def stop(self):
        """Stop the token refresh thread."""
        if self.refresh_thread and self.refresh_thread.is_alive():
            logger.info("Stopping token refresh thread")
            self.stop_event.set()
            self.refresh_thread.join(timeout=10)
            self.refresh_thread = None
            return True
        else:
            logger.info("Token refresh thread is not running")
            return False

    def _calculate_next_refresh_delay(self):
        """Calculate the next refresh delay with exponential backoff on failures."""
        base_delay = self.refresh_interval

        if self.consecutive_failures > 0:
            # Exponential backoff: 2^failures minutes, max 2 hours
            backoff_multiplier = min(2 ** self.consecutive_failures, 240)  # max 4 hours
            delay = min(base_delay * backoff_multiplier, 7200)  # max 2 hours
            logger.warning(f"Using backoff delay: {delay}s due to {self.consecutive_failures} consecutive failures")
            return delay

        return base_delay

    def _should_refresh_now(self):
        """Check if we should refresh the token now."""
        try:
            from . import token_store

            # Check if tokens exist
            if not token_store.has_tokens():
                logger.warning("No tokens available, need to refresh")
                return True

            # Check if token is expired or will expire soon
            if token_store.is_token_expired():
                logger.info("Token is expired or expiring soon, need to refresh")
                return True

            return False
        except Exception as e:
            logger.error(f"Error checking if refresh needed: {e}")
            return True  # When in doubt, try to refresh

    def _refresh_loop(self):
        """Main refresh loop that runs in a separate thread."""
        logger.info(f"Token refresh thread started on dyno {self.heroku_dyno_id}")

        while not self.stop_event.is_set():
            try:
                # Check if we need to refresh
                if self._should_refresh_now():
                    logger.info("Attempting token refresh...")
                    success = self._attempt_refresh()

                    if success:
                        self.last_refresh_time = datetime.now()
                        self.consecutive_failures = 0
                        logger.info(f"Token refresh successful at {self.last_refresh_time}")

                        # Record successful refresh
                        try:
                            from . import token_store
                            token_store.record_refresh_attempt(success=True)
                        except Exception as e:
                            logger.error(f"Error recording successful refresh: {e}")
                    else:
                        self.consecutive_failures += 1
                        logger.error(f"Token refresh failed (attempt {self.consecutive_failures})")

                        # Record failed refresh
                        try:
                            from . import token_store
                            token_store.record_refresh_attempt(success=False)
                        except Exception as e:
                            logger.error(f"Error recording failed refresh: {e}")

                        # If we've failed too many times, try to re-initialize from settings
                        if self.consecutive_failures >= self.max_failures:
                            logger.warning(f"Too many consecutive failures ({self.consecutive_failures}), attempting re-initialization")
                            self._attempt_reinitialize()

                # Calculate next refresh delay
                delay = self._calculate_next_refresh_delay()
                logger.debug(f"Next token refresh in {delay} seconds")

                # Wait for the delay or until stop is called
                self.stop_event.wait(delay)

            except Exception as e:
                logger.error(f"Unexpected error in refresh loop: {e}")
                # Wait a bit before retrying
                self.stop_event.wait(60)

        logger.info("Token refresh thread stopped")

    def _attempt_refresh(self):
        """Attempt to refresh the token."""
        try:
            return self.api_client.refresh_token()
        except Exception as e:
            logger.error(f"Error during token refresh: {e}")
            return False

    def _attempt_reinitialize(self):
        """Attempt to reinitialize tokens from settings."""
        try:
            logger.info("Attempting to reinitialize tokens from settings")

            # Get tokens from settings
            access_token = getattr(settings, 'REVIZTO_ACCESS_TOKEN', '')
            refresh_token = getattr(settings, 'REVIZTO_REFRESH_TOKEN', '')
            licence_uuid = getattr(settings, 'REVIZTO_LICENCE_UUID', '')

            if all([access_token, refresh_token, licence_uuid]):
                # Re-initialize the API client
                self.api_client.initialize(access_token, refresh_token, licence_uuid)
                logger.info("Successfully reinitialized tokens from settings")
                self.consecutive_failures = 0
                return True
            else:
                logger.error("Cannot reinitialize - missing tokens in settings")
                return False

        except Exception as e:
            logger.error(f"Error during token reinitialization: {e}")
            return False

    def get_status(self):
        """Get the current status of the token refresher."""
        try:
            from . import token_store
            token_status = token_store.get_token_status()
        except Exception as e:
            token_status = {"error": str(e)}

        return {
            "thread_alive": self.refresh_thread.is_alive() if self.refresh_thread else False,
            "last_refresh_time": self.last_refresh_time,
            "consecutive_failures": self.consecutive_failures,
            "is_heroku": self.is_heroku,
            "dyno_id": self.heroku_dyno_id,
            "refresh_interval": self.refresh_interval,
            "token_status": token_status,
        }

# Global instance
refresher = None

def initialize(api_client):
    """Initialize the token refresher with the API client."""
    # Check if token refresh is enabled in settings
    token_refresh_enabled = getattr(settings, 'REVIZTO_ENABLE_TOKEN_REFRESH', True)

    if not token_refresh_enabled:
        logger.info("Token refresh is disabled in settings. Skipping token refresher initialization.")
        return False

    global refresher
    if refresher is None:
        refresher = HerokuTokenRefresher(api_client)
        return refresher.start()
    else:
        # If refresher exists but thread is dead, restart it
        if not refresher.refresh_thread or not refresher.refresh_thread.is_alive():
            logger.warning("Existing refresher thread is dead, restarting...")
            return refresher.start()

    return False

def stop():
    """Stop the token refresher if it's running."""
    global refresher
    if refresher:
        return refresher.stop()
    return False

def get_status():
    """Get the current status of the token refresher."""
    global refresher
    if refresher:
        return refresher.get_status()
    return {"error": "No refresher initialized"}

def restart_if_needed():
    """Restart the refresher if it's not running (useful for dyno restarts)."""
    global refresher
    if refresher:
        if not refresher.refresh_thread or not refresher.refresh_thread.is_alive():
            logger.info("Restarting token refresher after dyno restart")
            return refresher.start()
    return False