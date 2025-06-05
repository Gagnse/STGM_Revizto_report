class ProjectRouter:
    """
    Database router for core models
    Routes ProjectData to PostgreSQL and TokenStorage to PostgreSQL as well
    """

    def db_for_read(self, model, **hints):
        """
        Point operations on core models to the appropriate database
        """
        if model._meta.app_label == 'core':
            if model.__name__ in ['ProjectData', 'TokenStorage']:
                return 'postgres'
        return None

    def db_for_write(self, model, **hints):
        """
        Point operations on core models to the appropriate database
        """
        if model._meta.app_label == 'core':
            if model.__name__ in ['ProjectData', 'TokenStorage']:
                return 'postgres'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations involving core models
        """
        if obj1._meta.app_label == 'core' and obj2._meta.app_label == 'core':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that core models migrations go to the right database
        """
        if app_label == 'core':
            if model_name in ['projectdata', 'tokenstorage']:
                return db == 'postgres'
        return None