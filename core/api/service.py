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

    # 1. Update the ReviztoAPI.get method in core/api/client.py
    # Add this replacement for the get method

    @classmethod
    def get(cls, endpoint, params=None):
        """
        Make a GET request to the API.

        Args:
            endpoint (str): API endpoint
            params (dict, optional): Query parameters

        Returns:
            dict: Response data

        Raises:
            Exception: If the request fails
        """
        if not cls.ensure_token_valid():
            print(f"[DEBUG] Failed to obtain valid token for endpoint: {endpoint}")
            raise Exception("Failed to obtain valid token")

        url = f"{cls.BASE_URL}{endpoint}"
        print(f"[DEBUG] Making API request to: {url}")
        print(f"[DEBUG] With params: {params}")

        try:
            print(f"[DEBUG] Request headers: {cls.get_headers()}")
            response = requests.get(url, headers=cls.get_headers(), params=params)

            print(f"[DEBUG] Response status code: {response.status_code}")
            print(f"[DEBUG] Response headers: {response.headers}")

            # Print a sample of the response text
            print(f"[DEBUG] Response preview: {response.text[:200]}...")

            # Handle 401 or 403 (token expired or invalid)
            if response.status_code in (401, 403) or "-206" in response.text:
                print(f"[DEBUG] Token expired or invalid. Attempting refresh...")
                # Try to refresh the token and retry the request
                if cls.refresh_token():
                    print(f"[DEBUG] Token refreshed. Retrying request...")
                    # Retry with new token
                    response = requests.get(url, headers=cls.get_headers(), params=params)
                    print(f"[DEBUG] Retry response status: {response.status_code}")
                else:
                    print(f"[DEBUG] Token refresh failed.")
                    raise Exception("Token refresh failed")

            print(f"[DEBUG] Final response status: {response.status_code}")
            response.raise_for_status()
            json_response = response.json()
            print(
                f"[DEBUG] JSON response keys: {list(json_response.keys()) if isinstance(json_response, dict) else 'Not a dict'}")
            return json_response
        except Exception as e:
            import traceback
            print(f"[DEBUG] API GET request failed: {e}")
            print(f"[DEBUG] Error traceback: {traceback.format_exc()}")
            raise

    # 2. Update the get_projects method in core/api/service.py

    @classmethod
    def get_projects(cls):
        """Get a list of all projects."""
        print("\n[DEBUG] ==== STARTING GET_PROJECTS ====")
        try:
            if not ReviztoAPI.LICENCE_UUID:
                print("[DEBUG] REVIZTO_LICENCE_UUID is not set in settings")
                return []

            print(f"[DEBUG] Using license UUID: {ReviztoAPI.LICENCE_UUID}")

            # Use the correct endpoint that's working
            endpoint = f"license/{ReviztoAPI.LICENCE_UUID}/projects"
            print(f"[DEBUG] Using endpoint: {endpoint}")

            try:
                data = ReviztoAPI.get(endpoint)
                print("[DEBUG] API request successful")
            except Exception as e:
                print(f"[DEBUG] API request failed with exception: {e}")
                return []

            print(f"[DEBUG] Response data type: {type(data)}")

            # Extract projects from the specific response format
            projects = []

            if isinstance(data, dict):
                print(f"[DEBUG] Response keys: {list(data.keys())}")

                # Check if we have data key and it contains entities
                if 'data' in data and isinstance(data['data'], dict):
                    data_obj = data['data']
                    print(f"[DEBUG] Data object keys: {list(data_obj.keys())}")

                    # Check for entities key which should contain projects
                    if 'entities' in data_obj and isinstance(data_obj['entities'], list):
                        entities = data_obj['entities']
                        print(f"[DEBUG] Found {len(entities)} entities")

                        # Process each entity as a project
                        for entity in entities:
                            if isinstance(entity, dict):
                                print(f"[DEBUG] Processing entity with keys: {list(entity.keys())[:5]}...")
                                projects.append(Project(entity))

                                # Debug the first project
                                if len(projects) == 1:
                                    project_id = entity.get('id', 'unknown')
                                    project_title = entity.get('title', entity.get('name', 'Untitled'))
                                    print(f"[DEBUG] First project: ID={project_id}, Title={project_title}")

            print(f"[DEBUG] Found {len(projects)} projects")
            return projects
        except Exception as e:
            import traceback
            print(f"[DEBUG] Failed to get projects: {e}")
            print(f"[DEBUG] Exception traceback: {traceback.format_exc()}")
            return []

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

    @classmethod
    def search_projects(cls, query):
        """Search for projects by title."""
        print(f"[DEBUG] Starting search for projects with query: {query}")
        try:
            # Get all projects
            projects = cls.get_projects()
            print(f"[DEBUG] Found {len(projects)} projects to search through")

            # Filter projects by title containing the query (case insensitive)
            if query:
                filtered_projects = []
                for project in projects:
                    project_title = project.name.lower()
                    if query.lower() in project_title:
                        print(f"[DEBUG] Match found: {project.name}")
                        filtered_projects.append(project)

                print(f"[DEBUG] Search returned {len(filtered_projects)} results")
                return filtered_projects

            return projects
        except Exception as e:
            import traceback
            print(f"[DEBUG] Failed to search projects: {e}")
            print(f"[DEBUG] Exception traceback: {traceback.format_exc()}")
            return []

    @classmethod
    def get_observations(cls, project_id):
        """Get all observations for a project (issues with stamp A-OB)."""
        print(f"[DEBUG] Fetching observations for project ID: {project_id}")
        try:
            endpoint = f"project/{project_id}/issue-filter/filter"
            params = {
                "anyFiltersDTO[0][type]": "stampAbbr",
                "anyFiltersDTO[0][expr]": "1",
                "anyFiltersDTO[0][value][2]": "A-OB",
                "sendFullIssueData": "true",
                "reportSort[1][field]": "sheet",
                "reportSort[1][direction]": "asc",
                "reportSort[2][field]": "id",
                "reportSort[2][direction]": "asc"
            }

            response = ReviztoAPI.get(endpoint, params=params)
            print(f"[DEBUG] Observations API response received: {type(response)}")

            # Pass through the raw API response
            return response

        except Exception as e:
            import traceback
            print(f"[DEBUG] Failed to get observations: {e}")
            print(f"[DEBUG] Exception traceback: {traceback.format_exc()}")
            return {"result": 1, "message": str(e), "data": {"data": []}}

    @classmethod
    def get_instructions(cls, project_id):
        """Get all instructions for a project (issues with stamp A-IN)."""
        print(f"[DEBUG] Fetching instructions for project ID: {project_id}")
        try:
            endpoint = f"project/{project_id}/issue-filter/filter"
            params = {
                "anyFiltersDTO[0][type]": "stampAbbr",
                "anyFiltersDTO[0][expr]": "1",
                "anyFiltersDTO[0][value][1]": "A-IN",
                "sendFullIssueData": "true",
                "reportSort[1][field]": "sheet",
                "reportSort[1][direction]": "asc",
                "reportSort[2][field]": "id",
                "reportSort[2][direction]": "asc"
            }

            response = ReviztoAPI.get(endpoint, params=params)
            print(f"[DEBUG] Instructions API response received: {type(response)}")

            # Pass through the raw API response
            return response

        except Exception as e:
            import traceback
            print(f"[DEBUG] Failed to get instructions: {e}")
            print(f"[DEBUG] Exception traceback: {traceback.format_exc()}")
            return {"result": 1, "message": str(e), "data": {"data": []}}

    @classmethod
    def get_deficiencies(cls, project_id):
        """Get all deficiencies for a project (issues with stamp A-DF)."""
        print(f"\n[DEBUG-SERVICE] ===== FETCHING DEFICIENCIES =====")
        print(f"[DEBUG-SERVICE] Fetching deficiencies for project ID: {project_id}")
        try:
            endpoint = f"project/{project_id}/issue-filter/filter"
            params = {
                "anyFiltersDTO[0][type]": "stampAbbr",
                "anyFiltersDTO[0][expr]": "1",
                "anyFiltersDTO[0][value][0]": "A-DF",
                "sendFullIssueData": "true",
                "reportSort[1][field]": "sheet",
                "reportSort[1][direction]": "asc",
                "reportSort[2][field]": "id",
                "reportSort[2][direction]": "asc"
            }

            print(f"[DEBUG-SERVICE] Using endpoint: {endpoint}")
            print(f"[DEBUG-SERVICE] Using params: {params}")

            # Make the API request
            try:
                response = ReviztoAPI.get(endpoint, params=params)
                print(f"[DEBUG-SERVICE] API call successful")
            except Exception as e:
                print(f"[DEBUG-SERVICE] API call failed: {e}")
                import traceback
                print(f"[DEBUG-SERVICE] API error traceback: {traceback.format_exc()}")
                return {"result": 1, "message": str(e), "data": {"data": []}}

            # Debug the response
            print(f"[DEBUG-SERVICE] Response type: {type(response)}")
            if isinstance(response, dict):
                print(f"[DEBUG-SERVICE] Response has keys: {list(response.keys())}")
                if 'result' in response:
                    print(f"[DEBUG-SERVICE] Result value: {response['result']}")

                # Check for data
                if 'data' in response:
                    data_obj = response['data']
                    if isinstance(data_obj, dict) and 'data' in data_obj:
                        deficiencies = data_obj['data']
                        print(f"[DEBUG-SERVICE] Found {len(deficiencies)} deficiencies")

                        # Debug first deficiency
                        if len(deficiencies) > 0:
                            first = deficiencies[0]
                            print(f"[DEBUG-SERVICE] First deficiency ID: {first.get('id')}")
                            print(f"[DEBUG-SERVICE] First deficiency has keys: {list(first.keys())[:10]}...")

            print(f"[DEBUG-SERVICE] ===== END FETCHING DEFICIENCIES =====\n")

            # Return the original response
            return response

        except Exception as e:
            print(f"[DEBUG-SERVICE] General error in get_deficiencies: {e}")
            import traceback
            print(f"[DEBUG-SERVICE] Exception traceback: {traceback.format_exc()}")
            return {"result": 1, "message": str(e), "data": {"data": []}}