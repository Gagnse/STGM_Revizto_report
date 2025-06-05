# core/api/token_store.py - Replace your existing file

"""
A persistent token store using database storage to survive dyno restarts.
"""

import logging
from django.db import transaction
from django.utils import timezone

logger = logging.getLogger(__name__)

def get_token_storage():
    """Get the token storage instance"""
    try:
        from core.models import TokenStorage
        return TokenStorage.get_instance()
    except Exception as e:
        logger.error(f"Error accessing token storage: {e}")
        return None

def set_tokens(access_token, refresh_token, licence_uuid, token_expiry=None, expires_in=3600):
    """Set all tokens at once."""
    try:
        with transaction.atomic():
            storage = get_token_storage()
            if storage:
                if token_expiry:
                    # If token_expiry is provided as datetime
                    storage.access_token = access_token
                    storage.refresh_token = refresh_token
                    storage.licence_uuid = licence_uuid
                    storage.token_expiry = token_expiry
                    storage.last_successful_refresh = timezone.now()
                    storage.refresh_failure_count = 0
                    storage.save()
                else:
                    # Use expires_in seconds
                    storage.update_tokens(access_token, refresh_token, licence_uuid, expires_in)
                
                logger.info("Tokens successfully stored in database")
                return True
    except Exception as e:
        logger.error(f"Error storing tokens: {e}")
    
    return False

def get_access_token():
    """Get the current access token."""
    try:
        storage = get_token_storage()
        return storage.access_token if storage else None
    except Exception as e:
        logger.error(f"Error getting access token: {e}")
        return None

def get_refresh_token():
    """Get the current refresh token."""
    try:
        storage = get_token_storage()
        return storage.refresh_token if storage else None
    except Exception as e:
        logger.error(f"Error getting refresh token: {e}")
        return None

def get_licence_uuid():
    """Get the current license UUID."""
    try:
        storage = get_token_storage()
        return storage.licence_uuid if storage else None
    except Exception as e:
        logger.error(f"Error getting licence UUID: {e}")
        return None

def get_token_expiry():
    """Get the current token expiry time."""
    try:
        storage = get_token_storage()
        return storage.token_expiry if storage else None
    except Exception as e:
        logger.error(f"Error getting token expiry: {e}")
        return None

def has_tokens():
    """Check if all required tokens are available."""
    try:
        storage = get_token_storage()
        if not storage:
            return False
        
        return bool(storage.access_token and storage.refresh_token and storage.licence_uuid)
    except Exception as e:
        logger.error(f"Error checking token availability: {e}")
        return False

def is_token_expired():
    """Check if the current token is expired or will expire soon."""
    try:
        storage = get_token_storage()
        if not storage:
            return True
        
        return storage.is_token_expired()
    except Exception as e:
        logger.error(f"Error checking token expiry: {e}")
        return True

def update_access_token(new_token, expires_in=3600):
    """Update only the access token."""
    try:
        with transaction.atomic():
            storage = get_token_storage()
            if storage:
                storage.access_token = new_token
                storage.token_expiry = timezone.now() + timezone.timedelta(seconds=expires_in)
                storage.last_successful_refresh = timezone.now()
                storage.refresh_failure_count = 0
                storage.save()
                return True
    except Exception as e:
        logger.error(f"Error updating access token: {e}")
    
    return False

def update_refresh_token(new_token):
    """Update only the refresh token."""
    try:
        with transaction.atomic():
            storage = get_token_storage()
            if storage:
                storage.refresh_token = new_token
                storage.save()
                return True
    except Exception as e:
        logger.error(f"Error updating refresh token: {e}")
    
    return False

def record_refresh_attempt(success=False):
    """Record a token refresh attempt"""
    try:
        storage = get_token_storage()
        if storage:
            storage.record_refresh_attempt(success)
    except Exception as e:
        logger.error(f"Error recording refresh attempt: {e}")

def get_token_status():
    """Get comprehensive token status for debugging"""
    try:
        storage = get_token_storage()
        if not storage:
            return {"error": "No token storage available"}
        
        return {
            "has_access_token": bool(storage.access_token),
            "has_refresh_token": bool(storage.refresh_token),
            "has_licence_uuid": bool(storage.licence_uuid),
            "token_expiry": storage.token_expiry,
            "is_expired": storage.is_token_expired(),
            "last_refresh_attempt": storage.last_refresh_attempt,
            "last_successful_refresh": storage.last_successful_refresh,
            "refresh_failure_count": storage.refresh_failure_count,
            "created_at": storage.created_at,
            "updated_at": storage.updated_at,
        }
    except Exception as e:
        return {"error": str(e)}