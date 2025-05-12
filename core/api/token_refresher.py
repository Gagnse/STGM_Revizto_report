"""
Token refresh module for Revizto API.
This module automatically refreshes the Revizto API tokens every 30 minutes.
"""

import threading
import time
import logging
from datetime import datetime

# Create a logger for this module
logger = logging.getLogger(__name__)


class TokenRefresher:
    """
    Class to handle automatic refresh of Revizto API tokens.
    """

    def __init__(self, api_client, refresh_interval=1800):  # 1800 seconds = 30 minutes
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

    def start(self):
        """
        Start the token refresh thread if it's not already running.
        """
        if self.refresh_thread is None or not self.refresh_thread.is_alive():
            logger.info("Starting token refresh thread")
            self.stop_event.clear()
            self.refresh_thread = threading.Thread(target=self._refresh_loop)
            self.refresh_thread.daemon = True  # Make thread exit when main thread exits
            self.refresh_thread.start()
            return True
        else:
            logger.info("Token refresh thread is already running")
            return False

    def stop(self):
        """
        Stop the token refresh thread.
        """
        if self.refresh_thread and self.refresh_thread.is_alive():
            logger.info("Stopping token refresh thread")
            self.stop_event.set()
            self.refresh_thread.join(timeout=5)  # Wait up to 5 seconds for thread to exit
            self.refresh_thread = None
            return True
        else:
            logger.info("Token refresh thread is not running")
            return False

    def _refresh_loop(self):
        """
        Main refresh loop that runs in a separate thread.
        """
        logger.info("Token refresh thread started")

        while not self.stop_event.is_set():
            try:
                # Try to refresh the token
                success = self.api_client.refresh_token()

                if success:
                    self.last_refresh_time = datetime.now()
                    logger.info(f"Successfully refreshed token at {self.last_refresh_time}")
                else:
                    logger.error("Failed to refresh token")

            except Exception as e:
                logger.error(f"Error during token refresh: {e}")

            # Wait for the refresh interval or until stop is called
            self.stop_event.wait(self.refresh_interval)

        logger.info("Token refresh thread stopped")


# Global instance to be used by the application
refresher = None


def initialize(api_client):
    """
    Initialize the token refresher with the API client.

    Args:
        api_client: The ReviztoAPI client class
    """
    global refresher
    if refresher is None:
        refresher = TokenRefresher(api_client)
        return refresher.start()
    return False


def stop():
    """
    Stop the token refresher if it's running.
    """
    global refresher
    if refresher:
        return refresher.stop()
    return False