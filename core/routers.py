class ProjectRouter:
    """
    Database router for the ProjectData model
    Routes all operations for ProjectData to the PostgreSQL database
    """

    def db_for_read(self, model, **hints):
        """
        Point all operations on ProjectData model to the 'postgres' database
        """
        if model._meta.app_label == 'core' and model.__name__ == 'ProjectData':
            return 'postgres'
        return None

    def db_for_write(self, model, **hints):
        """
        Point all operations on ProjectData model to the 'postgres' database
        """
        if model._meta.app_label == 'core' and model.__name__ == 'ProjectData':
            return 'postgres'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations involving the ProjectData model
        """
        if obj1._meta.app_label == 'core' and obj2._meta.app_label == 'core':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the ProjectData model isn't created during migrations since it's using an existing table
        """
        if app_label == 'core' and model_name == 'projectdata':
            return False
        return None