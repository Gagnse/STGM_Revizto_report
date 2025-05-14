"""
A singleton store for API tokens to ensure persistence across requests.
"""

# Token storage - use module-level variables for persistence
ACCESS_TOKEN = None
REFRESH_TOKEN = None
LICENCE_UUID = None
TOKEN_EXPIRY = None


def set_tokens(access_token, refresh_token, licence_uuid, token_expiry):
    """Set all tokens at once."""
    global ACCESS_TOKEN, REFRESH_TOKEN, LICENCE_UUID, TOKEN_EXPIRY
    ACCESS_TOKEN = access_token
    REFRESH_TOKEN = refresh_token
    LICENCE_UUID = licence_uuid
    TOKEN_EXPIRY = token_expiry

    # Debug
    print(f"[DEBUG] Tokens set in token_store module:")
    print(
        f"[DEBUG] - Access token: {'Set' if ACCESS_TOKEN else 'Not set'} (Length: {len(ACCESS_TOKEN) if ACCESS_TOKEN else 0})")
    print(
        f"[DEBUG] - Refresh token: {'Set' if REFRESH_TOKEN else 'Not set'} (Length: {len(REFRESH_TOKEN) if REFRESH_TOKEN else 0})")
    print(
        f"[DEBUG] - License UUID: {'Set' if LICENCE_UUID else 'Not set'} (Length: {len(LICENCE_UUID) if LICENCE_UUID else 0})")

    return True


def get_access_token():
    """Get the current access token."""
    return ACCESS_TOKEN


def get_refresh_token():
    """Get the current refresh token."""
    return REFRESH_TOKEN


def get_licence_uuid():
    """Get the current license UUID."""
    return LICENCE_UUID


def get_token_expiry():
    """Get the current token expiry time."""
    return TOKEN_EXPIRY


def has_tokens():
    """Check if all tokens are available."""
    return bool(ACCESS_TOKEN and REFRESH_TOKEN and LICENCE_UUID)


def update_access_token(new_token):
    """Update only the access token."""
    global ACCESS_TOKEN
    ACCESS_TOKEN = new_token
    return True


def update_refresh_token(new_token):
    """Update only the refresh token."""
    global REFRESH_TOKEN
    REFRESH_TOKEN = new_token
    return True


def update_token_expiry(new_expiry):
    """Update only the token expiry time."""
    global TOKEN_EXPIRY
    TOKEN_EXPIRY = new_expiry
    return True