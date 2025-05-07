from django.db import models

class ProjectData(models.Model):
    """
    Model for storing project information in the database
    Maps to the 'projets' table in MySQL
    """
    id = models.CharField(max_length=255, primary_key=True)
    noDossier = models.CharField(max_length=255, null=True, blank=True)
    noProjet = models.CharField(max_length=255, null=True, blank=True)
    maitreOuvragge = models.CharField(max_length=255, null=True, blank=True)
    entrepreneur = models.CharField(max_length=255, null=True, blank=True)
    noVisite = models.CharField(max_length=255, null=True, blank=True)
    visitePar = models.CharField(max_length=255, null=True, blank=True)
    dateVisite = models.DateTimeField(null=True, blank=True)
    presence = models.CharField(max_length=255, null=True, blank=True)
    rapportDate = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    distribution = models.CharField(max_length=500, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = False  # Use existing table
        db_table = 'projets'  # Use the actual table name from your MySQL schema