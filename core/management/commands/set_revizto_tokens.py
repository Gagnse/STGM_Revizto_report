from django.core.management.base import BaseCommand
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from django.conf import settings
from core.api.token_manager import TokenManager


class Command(BaseCommand):
    help = 'Sets initial Revizto API tokens manually'

    def add_arguments(self, parser):
        parser.add_argument('--access-token', type=str, help='Revizto API access token')
        parser.add_argument('--refresh-token', type=str, help='Revizto API refresh token')
        parser.add_argument('--from-env', action='store_true', help='Load tokens from environment variables')

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Setting up Revizto API tokens'))

        access_token = options.get('access_token')
        refresh_token = options.get('refresh_token')
        from_env = options.get('from_env')

        if from_env:
            # Get tokens from environment
            access_token = os.environ.get('REVIZTO_ACCESS_TOKEN')
            refresh_token = os.environ.get('REVIZTO_REFRESH_TOKEN')

            if not access_token or not refresh_token:
                self.stdout.write(self.style.ERROR(
                    'No tokens found in environment variables. Please set REVIZTO_ACCESS_TOKEN and REVIZTO_REFRESH_TOKEN.'))
                return

            self.stdout.write(self.style.SUCCESS('Using tokens from environment variables'))
        else:
            # Validate input tokens
            if not access_token or not refresh_token:
                self.stdout.write(self.style.ERROR('Both --access-token and --refresh-token are required'))
                return

        try:
            # Set the tokens directly using TokenManager's internal storage file
            token_file = TokenManager.TOKEN_FILE

            # Calculate expiry (1 hour from now)
            token_expiry = datetime.now() + timedelta(hours=1)

            token_data = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_expiry': token_expiry.isoformat(),
                'updated_at': datetime.now().isoformat()
            }

            # Create the file with restricted permissions
            with open(token_file, 'w') as f:
                json.dump(token_data, f)

            # Set file permissions to be readable only by the owner
            os.chmod(token_file, 0o600)

            self.stdout.write(self.style.SUCCESS(f'Tokens successfully saved to {token_file}'))

            # Safely print partial tokens
            safe_access_token = f"{access_token[:10]}...{access_token[-5:]}"
            safe_refresh_token = f"{refresh_token[:10]}...{refresh_token[-5:]}"

            self.stdout.write(f"Access Token: {safe_access_token}")
            self.stdout.write(f"Refresh Token: {safe_refresh_token}")
            self.stdout.write(f"Valid until: {token_expiry}")

            # Reinitialize TokenManager
            TokenManager._initialized = False
            TokenManager.initialize()

            self.stdout.write(self.style.SUCCESS('TokenManager reinitialized with the new tokens'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error setting tokens: {e}'))