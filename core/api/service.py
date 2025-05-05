import logging
from .client import ReviztoAPI
from .models import Project, Issue, User

logger = logging.getLogger(__name__)


class ReviztoService:
    """Service for retrieving data from the Revizto API."""

    @classmethod
    def get_projects(cls):
        """Get a list of all projects."""
        try:
            data = ReviztoAPI.get("projects")

            projects = []
            for item in data.get("items", []):
                projects.append(Project(item))

            return projects
        except Exception as e:
            logger.error(f"Failed to get projects: {e}")
            return []

    @classmethod
    def get_project(cls, project_id):
        """Get a specific project by ID."""
        try:
            data = ReviztoAPI.get(f"projects/{project_id}")
            return Project(data)
        except Exception as e:
            logger.error(f"Failed to get project {project_id}: {e}")
            return None

    @classmethod
    def get_issues(cls, project_id, status=None):
        """Get issues for a project with optional status filter."""
        try:
            params = {}
            if status:
                params["status"] = status

            data = ReviztoAPI.get(f"projects/{project_id}/issues", params=params)

            issues = []
            for item in data.get("items", []):
                issues.append(Issue(item))

            return issues
        except Exception as e:
            logger.error(f"Failed to get issues for project {project_id}: {e}")
            return []

    @classmethod
    def get_issue(cls, project_id, issue_id):
        """Get a specific issue by ID."""
        try:
            data = ReviztoAPI.get(f"projects/{project_id}/issues/{issue_id}")
            return Issue(data)
        except Exception as e:
            logger.error(f"Failed to get issue {issue_id}: {e}")
            return None

    @classmethod
    def get_users(cls):
        """Get a list of all users."""
        try:
            data = ReviztoAPI.get("users")

            users = []
            for item in data.get("items", []):
                users.append(User(item))

            return users
        except Exception as e:
            logger.error(f"Failed to get users: {e}")
            return []

    @classmethod
    def get_user(cls, user_id):
        """Get a specific user by ID."""
        try:
            data = ReviztoAPI.get(f"users/{user_id}")
            return User(data)
        except Exception as e:
            logger.error(f"Failed to get user {user_id}: {e}")
            return None

    # Add more service methods based on your needs