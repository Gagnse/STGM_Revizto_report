# core/api/token_store.py - Fixed version with proper PostgreSQL database usage

"""
A persistent token store using PostgreSQL database storage to survive dyno restarts.
"""

import logging
from django.db import transaction
from django.utils import timezone

logger = logging.getLogger(__name__)


def get_token_storage():
    """Get the token storage instance from PostgreSQL database"""
    try:
        from core.models import TokenStorage
        return TokenStorage.get_instance()
    except Exception as e:
        logger.error(f"Error accessing token storage: {e}")
        return None


def set_tokens(access_token, refresh_token, licence_uuid, token_expiry=None, expires_in=3600):
    """Set all tokens at once in PostgreSQL database."""
    try:
        # Use atomic transaction on postgres database
        with transaction.atomic(using='postgres'):
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
                    storage.save(using='postgres')
                else:
                    # Use expires_in seconds
                    storage.update_tokens(access_token, refresh_token, licence_uuid, expires_in)

                logger.info("Tokens successfully stored in PostgreSQL database")
                print(
                    f"[TOKEN-STORE] Tokens saved to PostgreSQL - Access: {len(access_token)} chars, Refresh: {len(refresh_token)} chars")
                return True
            else:
                logger.error("Could not get token storage instance")
                return False
    except Exception as e:
        logger.error(f"Error storing tokens: {e}")
        print(f"[TOKEN-STORE] Error storing tokens: {e}")

    return False


def get_access_token():
    """Get the current access token from PostgreSQL database."""
    try:
        storage = get_token_storage()
        if storage and storage.access_token:
            print(f"[TOKEN-STORE] Retrieved access token from PostgreSQL ({len(storage.access_token)} chars)")
            return storage.access_token
        else:
            print(f"[TOKEN-STORE] No access token found in PostgreSQL")
            return None
    except Exception as e:
        logger.error(f"Error getting access token: {e}")
        print(f"[TOKEN-STORE] Error getting access token: {e}")
        return None


def get_refresh_token():
    """Get the current refresh token from PostgreSQL database."""
    try:
        storage = get_token_storage()
        if storage and storage.refresh_token:
            print(f"[TOKEN-STORE] Retrieved refresh token from PostgreSQL ({len(storage.refresh_token)} chars)")
            return storage.refresh_token
        else:
            print(f"[TOKEN-STORE] No refresh token found in PostgreSQL")
            return None
    except Exception as e:
        logger.error(f"Error getting refresh token: {e}")
        print(f"[TOKEN-STORE] Error getting refresh token: {e}")
        return None


def get_licence_uuid():
    """Get the current license UUID from PostgreSQL database."""
    try:
        storage = get_token_storage()
        if storage and storage.licence_uuid:
            print(f"[TOKEN-STORE] Retrieved licence UUID from PostgreSQL: {storage.licence_uuid}")
            return storage.licence_uuid
        else:
            print(f"[TOKEN-STORE] No licence UUID found in PostgreSQL")
            return None
    except Exception as e:
        logger.error(f"Error getting licence UUID: {e}")
        print(f"[TOKEN-STORE] Error getting licence UUID: {e}")
        return None


def get_token_expiry():
    """Get the current token expiry time from PostgreSQL database."""
    try:
        storage = get_token_storage()
        if storage:
            print(f"[TOKEN-STORE] Token expiry from PostgreSQL: {storage.token_expiry}")
            return storage.token_expiry
        else:
            print(f"[TOKEN-STORE] No token expiry found in PostgreSQL")
            return None
    except Exception as e:
        logger.error(f"Error getting token expiry: {e}")
        print(f"[TOKEN-STORE] Error getting token expiry: {e}")
        return None


def has_tokens():
    """Check if all required tokens are available in PostgreSQL database."""
    try:
        storage = get_token_storage()
        if not storage:
            print(f"[TOKEN-STORE] No token storage instance available")
            return False

        has_all = bool(storage.access_token and storage.refresh_token and storage.licence_uuid)
        print(f"[TOKEN-STORE] Token availability check: {has_all}")
        print(f"[TOKEN-STORE] - Access token: {'✅' if storage.access_token else '❌'}")
        print(f"[TOKEN-STORE] - Refresh token: {'✅' if storage.refresh_token else '❌'}")
        print(f"[TOKEN-STORE] - Licence UUID: {'✅' if storage.licence_uuid else '❌'}")
        return has_all
    except Exception as e:
        logger.error(f"Error checking token availability: {e}")
        print(f"[TOKEN-STORE] Error checking token availability: {e}")
        return False


def is_token_expired():
    """Check if the current token is expired or will expire soon."""
    try:
        storage = get_token_storage()
        if not storage:
            print(f"[TOKEN-STORE] No token storage instance, considering expired")
            return True

        expired = storage.is_token_expired()
        print(f"[TOKEN-STORE] Token expiry check: {'🔴 Expired' if expired else '🟢 Valid'}")
        if storage.token_expiry:
            print(f"[TOKEN-STORE] Expires at: {storage.token_expiry}")
        return expired
    except Exception as e:
        logger.error(f"Error checking token expiry: {e}")
        print(f"[TOKEN-STORE] Error checking token expiry: {e}")
        return True


def update_access_token(new_token, expires_in=3600):
    """Update only the access token in PostgreSQL database."""
    try:
        with transaction.atomic(using='postgres'):
            storage = get_token_storage()
            if storage:
                storage.access_token = new_token
                storage.token_expiry = timezone.now() + timezone.timedelta(seconds=expires_in)
                storage.last_successful_refresh = timezone.now()
                storage.refresh_failure_count = 0
                storage.save(using='postgres')
                print(f"[TOKEN-STORE] Access token updated in PostgreSQL")
                return True
            else:
                print(f"[TOKEN-STORE] Could not get storage instance for access token update")
                return False
    except Exception as e:
        logger.error(f"Error updating access token: {e}")
        print(f"[TOKEN-STORE] Error updating access token: {e}")

    return False


def update_refresh_token(new_token):
    """Update only the refresh token in PostgreSQL database."""
    try:
        with transaction.atomic(using='postgres'):
            storage = get_token_storage()
            if storage:
                storage.refresh_token = new_token
                storage.save(using='postgres')
                print(f"[TOKEN-STORE] Refresh token updated in PostgreSQL")
                return True
            else:
                print(f"[TOKEN-STORE] Could not get storage instance for refresh token update")
                return False
    except Exception as e:
        logger.error(f"Error updating refresh token: {e}")
        print(f"[TOKEN-STORE] Error updating refresh token: {e}")

    return False


def record_refresh_attempt(success=False):
    """Record a token refresh attempt in PostgreSQL database"""
    try:
        storage = get_token_storage()
        if storage:
            storage.record_refresh_attempt(success)
            print(f"[TOKEN-STORE] Refresh attempt recorded: {'✅ Success' if success else '❌ Failed'}")
        else:
            print(f"[TOKEN-STORE] Could not record refresh attempt - no storage instance")
    except Exception as e:
        logger.error(f"Error recording refresh attempt: {e}")
        print(f"[TOKEN-STORE] Error recording refresh attempt: {e}")


def get_token_status():
    """Get comprehensive token status for debugging"""
    try:
        storage = get_token_storage()
        if not storage:
            return {"error": "No token storage available"}

        status = {
            "has_access_token": bool(storage.access_token),
            "access_token_length": len(storage.access_token) if storage.access_token else 0,
            "has_refresh_token": bool(storage.refresh_token),
            "refresh_token_length": len(storage.refresh_token) if storage.refresh_token else 0,
            "has_licence_uuid": bool(storage.licence_uuid),
            "licence_uuid": storage.licence_uuid,
            "token_expiry": storage.token_expiry,
            "is_expired": storage.is_token_expired(),
            "last_refresh_attempt": storage.last_refresh_attempt,
            "last_successful_refresh": storage.last_successful_refresh,
            "refresh_failure_count": storage.refresh_failure_count,
            "created_at": storage.created_at,
            "updated_at": storage.updated_at,
        }

        print(f"[TOKEN-STORE] Status check completed:")
        print(f"[TOKEN-STORE] - Storage ID: {storage.id}")
        print(
            f"[TOKEN-STORE] - Has tokens: {status['has_access_token'] and status['has_refresh_token'] and status['has_licence_uuid']}")
        print(f"[TOKEN-STORE] - Token expired: {status['is_expired']}")
        print(f"[TOKEN-STORE] - Last successful refresh: {status['last_successful_refresh']}")

        return status
    except Exception as e:
        error_msg = f"Error getting token status: {e}"
        print(f"[TOKEN-STORE] {error_msg}")
        return {"error": error_msg}


def clear_all_tokens():
    """Clear all tokens from PostgreSQL database (for testing/debugging)"""
    try:
        storage = get_token_storage()
        if storage:
            storage.access_token = None
            storage.refresh_token = None
            storage.licence_uuid = None
            storage.token_expiry = None
            storage.save(using='postgres')
            print(f"[TOKEN-STORE] All tokens cleared from PostgreSQL")
            return True
        return False
    except Exception as e:
        logger.error(f"Error clearing tokens: {e}")
        print(f"[TOKEN-STORE] Error clearing tokens: {e}")
        return False