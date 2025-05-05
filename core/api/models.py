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

    @property
    def id(self):
        """Get the project ID."""
        return self._data.get('id')

    @property
    def name(self):
        """Get the project name/title."""
        # Try 'title' first (from your sample), then fall back to 'name'
        return self._data.get('title', self._data.get('name', 'Untitled Project'))

    @property
    def description(self):
        """Get the project description."""
        return self._data.get('description', '')

    @property
    def created_at(self):
        """Get project creation date."""
        return self._data.get('created', '')

    @property
    def updated_at(self):
        """Get project update date."""
        return self._data.get('updated', '')

    @property
    def owner(self):
        """Get project owner info."""
        owner_data = self._data.get('owner', {})
        if isinstance(owner_data, dict):
            return owner_data.get('fullname', 'Unknown')
        return 'Unknown'

    @property
    def preview_url(self):
        """Get project preview image URL."""
        return self._data.get('preview', '')


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