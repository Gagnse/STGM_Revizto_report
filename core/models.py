from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
import json

class ProjectData(models.Model):
    """
    Model for storing project information in the database
    Maps to the 'projets' table in PostgreSQL
    """
    id = models.CharField(max_length=255, primary_key=True)
    # Use db_column to specify the exact column names in PostgreSQL
    nodossier = models.CharField(max_length=255, null=True, blank=True, db_column='nodossier')
    noprojet = models.CharField(max_length=255, null=True, blank=True, db_column='noprojet')
    maitreouvragge = models.CharField(max_length=255, null=True, blank=True, db_column='maitreouvragge')
    entrepreneur = models.CharField(max_length=255, null=True, blank=True, db_column='entrepreneur')
    novisite = models.CharField(max_length=255, null=True, blank=True, db_column='novisite')
    visitepar = models.CharField(max_length=255, null=True, blank=True, db_column='visitepar')
    datevisite = models.DateTimeField(null=True, blank=True, db_column='datevisite')
    presence = models.CharField(max_length=255, null=True, blank=True, db_column='presence')
    rapportdate = models.DateTimeField(null=True, blank=True, db_column='rapportdate')
    description = models.CharField(max_length=500, null=True, blank=True, db_column='description')
    distribution = models.CharField(max_length=500, null=True, blank=True, db_column='distribution')
    image = models.TextField(null=True, blank=True, db_column='image')  # Changed to TextField for base64 images

    class Meta:
        managed = False  # Use existing table
        db_table = 'projets'  # Use the actual table name from your PostgreSQL schema


class TokenStorage(models.Model):
    """
    Persistent storage for API tokens that survives dyno restarts
    This will be stored in the PostgreSQL database, not SQLite
    """
    # Use a singleton pattern - only one row should exist
    id = models.AutoField(primary_key=True)

    # Token fields - use TextField for long tokens
    access_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)
    licence_uuid = models.CharField(max_length=255, blank=True, null=True)

    # Expiry tracking
    token_expiry = models.DateTimeField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Additional fields for monitoring
    last_refresh_attempt = models.DateTimeField(null=True, blank=True)
    last_successful_refresh = models.DateTimeField(null=True, blank=True)
    refresh_failure_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'revizto_tokens'
        # This model should use the PostgreSQL database
        app_label = 'core'

    @classmethod
    def get_instance(cls):
        """Get or create the singleton token storage instance"""
        try:
            # Use the postgres database explicitly
            instance, created = cls.objects.using('postgres').get_or_create(id=1)
            if created:
                print(f"[TOKEN-DB] Created new TokenStorage instance in PostgreSQL")
            else:
                print(f"[TOKEN-DB] Retrieved existing TokenStorage instance from PostgreSQL")
            return instance
        except Exception as e:
            print(f"[TOKEN-DB] Error accessing TokenStorage: {e}")
            # Try to create the table if it doesn't exist
            try:
                from django.db import connection
                with connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS revizto_tokens (
                            id SERIAL PRIMARY KEY,
                            access_token TEXT,
                            refresh_token TEXT,
                            licence_uuid VARCHAR(255),
                            token_expiry TIMESTAMP WITH TIME ZONE,
                            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                            last_refresh_attempt TIMESTAMP WITH TIME ZONE,
                            last_successful_refresh TIMESTAMP WITH TIME ZONE,
                            refresh_failure_count INTEGER DEFAULT 0
                        );
                    """)
                print(f"[TOKEN-DB] Created revizto_tokens table")
                # Try again after creating table
                instance, created = cls.objects.using('postgres').get_or_create(id=1)
                return instance
            except Exception as create_error:
                print(f"[TOKEN-DB] Error creating table: {create_error}")
                return None

    def is_token_expired(self):
        """Check if the current token is expired or will expire soon"""
        if not self.token_expiry:
            return True

        # Consider expired if expiring in next 5 minutes
        expiry_threshold = timezone.now() + timedelta(minutes=5)
        return self.token_expiry <= expiry_threshold

    def update_tokens(self, access_token, refresh_token=None, licence_uuid=None, expires_in=3600):
        """Update stored tokens"""
        self.access_token = access_token
        if refresh_token:
            self.refresh_token = refresh_token
        if licence_uuid:
            self.licence_uuid = licence_uuid

        # Set expiry
        self.token_expiry = timezone.now() + timedelta(seconds=expires_in)
        self.last_successful_refresh = timezone.now()
        self.refresh_failure_count = 0
        self.updated_at = timezone.now()

        # Save to PostgreSQL database
        self.save(using='postgres')
        print(f"[TOKEN-DB] Tokens updated in PostgreSQL, expire at: {self.token_expiry}")

    def record_refresh_attempt(self, success=False):
        """Record a token refresh attempt"""
        self.last_refresh_attempt = timezone.now()

        if success:
            self.last_successful_refresh = timezone.now()
            self.refresh_failure_count = 0
        else:
            self.refresh_failure_count += 1

        self.updated_at = timezone.now()
        # Save to PostgreSQL database
        self.save(using='postgres')

    def save(self, *args, **kwargs):
        """Override save to always use PostgreSQL database"""
        kwargs['using'] = 'postgres'
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Override delete to always use PostgreSQL database"""
        kwargs['using'] = 'postgres'
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"TokenStorage(expires: {self.token_expiry}, failures: {self.refresh_failure_count})"