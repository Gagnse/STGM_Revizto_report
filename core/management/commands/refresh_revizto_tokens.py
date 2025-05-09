from django.core.management.base import BaseCommand
from core.api.token_manager import TokenManager


class Command(BaseCommand):
    help = 'Refreshes Revizto API tokens'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting Revizto API token refresh'))

        try:
            # Initialize token manager if not already initialized
            if not TokenManager.is_valid():
                TokenManager.initialize()
                self.stdout.write(self.style.SUCCESS('TokenManager initialized'))

            # Perform token refresh
            if TokenManager.refresh_tokens():
                self.stdout.write(self.style.SUCCESS('Successfully refreshed Revizto API tokens'))

                # Show current tokens
                access_token = TokenManager.get_access_token()
                refresh_token = TokenManager.get_refresh_token()

                # Safely print partial tokens (first 10 chars + last 5 chars)
                self.stdout.write(f"Access Token: {access_token[:10]}...{access_token[-5:]}")
                self.stdout.write(f"Refresh Token: {refresh_token[:10]}...{refresh_token[-5:]}")

                self.stdout.write(self.style.SUCCESS('Tokens refreshed and ready to use'))
            else:
                self.stdout.write(self.style.ERROR('Failed to refresh tokens'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error refreshing tokens: {e}'))