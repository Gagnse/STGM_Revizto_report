from django.db import models

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
    image = models.CharField(max_length=255, null=True, blank=True, db_column='image')

    class Meta:
        managed = False  # Use existing table
        db_table = 'projets'  # Use the actual table name from your PostgreSQL schema