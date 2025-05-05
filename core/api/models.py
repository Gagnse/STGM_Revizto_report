class ApiModel:
    """Base class for API models."""

    def __init__(self, data=None):
        """
        Initialize from API data.

        Args:
            data (dict): Raw API data
        """
        self._data = data or {}

        # Set attributes from data
        for key, value in self._data.items():
            setattr(self, key, value)

    @property
    def raw_data(self):
        """Get the raw data dictionary."""
        return self._data


class Project(ApiModel):
    """Represents a Revizto project."""
    pass


class Issue(ApiModel):
    """Represents a Revizto issue."""
    pass


class User(ApiModel):
    """Represents a Revizto user."""

    @property
    def full_name(self):
        """Get the user's full name."""
        first_name = getattr(self, 'first_name', '')
        last_name = getattr(self, 'last_name', '')

        if first_name and last_name:
            return f"{first_name} {last_name}"
        return getattr(self, 'username', 'Unknown')

# Add more models as needed based on the API response structure