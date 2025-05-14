import logging
from .client import ReviztoAPI
from .models import Project, Issue, User
from . import token_store  # Import the token store

logger = logging.getLogger(__name__)


class ReviztoService:
    """Service for retrieving data from the Revizto API."""

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
        # Verify tokens are available before making request
        if not token_store.has_tokens():
            print(f"[DEBUG] Token store is missing tokens, aborting request to: {endpoint}")
            raise Exception("API tokens not available")

        # Forward to ReviztoAPI
        return ReviztoAPI.get(endpoint, params)

    @classmethod
    def get_projects(cls):
        """Get a list of all projects."""
        print("\n[DEBUG] ==== STARTING GET_PROJECTS ====")
        try:
            # Get license UUID from token store
            licence_uuid = token_store.get_licence_uuid()
            if not licence_uuid:
                # Fallback to settings if token store doesn't have it
                from django.conf import settings
                licence_uuid = settings.REVIZTO_LICENCE_UUID

            if not licence_uuid:
                print("[DEBUG] REVIZTO_LICENCE_UUID is not set in settings or token store")
                return []

            print(f"[DEBUG] Using license UUID: {licence_uuid}")
            print(
                f"[DEBUG] Token state: access={bool(token_store.get_access_token())}, refresh={bool(token_store.get_refresh_token())}")

            # Use the correct endpoint that's working
            endpoint = f"license/{licence_uuid}/projects"
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
            # Verify tokens are available before making request
            if not token_store.has_tokens():
                logger.error("Token store is missing tokens, aborting issues request")
                return []

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
            # Verify tokens are available before making request
            if not token_store.has_tokens():
                logger.error("Token store is missing tokens, aborting issue details request")
                return None

            data = ReviztoAPI.get(f"projects/{project_id}/issues/{issue_id}")
            return Issue(data)
        except Exception as e:
            logger.error(f"Failed to get issue {issue_id}: {e}")
            return None

    @classmethod
    def get_users(cls):
        """Get a list of all users."""
        try:
            # Verify tokens are available before making request
            if not token_store.has_tokens():
                logger.error("Token store is missing tokens, aborting users request")
                return []

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
            # Verify tokens are available before making request
            if not token_store.has_tokens():
                logger.error("Token store is missing tokens, aborting user details request")
                return None

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
            # Verify tokens are available before making request
            if not token_store.has_tokens():
                print(f"[DEBUG] Token store is missing tokens, aborting projects search")
                return []

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
            # Verify tokens are available before making request
            if not token_store.has_tokens():
                print(f"[DEBUG] Token store is missing tokens, aborting observations request")
                return {"result": 1, "message": "API tokens not available", "data": {"data": []}}

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
            # Verify tokens are available before making request
            if not token_store.has_tokens():
                print(f"[DEBUG] Token store is missing tokens, aborting instructions request")
                return {"result": 1, "message": "API tokens not available", "data": {"data": []}}

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
            # Verify tokens are available before making request
            if not token_store.has_tokens():
                print(f"[DEBUG-SERVICE] Token store is missing tokens, aborting deficiencies request")
                return {"result": 1, "message": "API tokens not available", "data": {"data": []}}

            endpoint = f"project/{project_id}/issue-filter/filter"
            params = {
                "anyFiltersDTO[0][type]": "stampAbbr",
                "anyFiltersDTO[0][expr]": "1",
                "anyFiltersDTO[0][value][0]": "A-DF",
                "sendFullIssueData": "true",
                "reportSort[2][field]": "sheet",
                "reportSort[2][direction]": "asc",
                "reportSort[3][field]": "id",
                "reportSort[3][direction]": "asc",
            }

            print(f"[DEBUG-SERVICE] Using endpoint: {endpoint}")
            print(f"[DEBUG-SERVICE] Using params: {params}")
            print(
                f"[DEBUG-SERVICE] Token state: access={bool(token_store.get_access_token())}, refresh={bool(token_store.get_refresh_token())}")

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

    @classmethod
    def get_issue_comments(cls, project_id, issue_id, date):
        """
        Get comments history for a specific issue.

        Args:
            project_id (int): Project ID
            issue_id (int): Issue ID
            date (str): Date in YYYY-MM-DD format to filter comments

        Returns:
            dict: Response with comments data
        """
        print(f"\n[DEBUG-SERVICE] ===== FETCHING ISSUE COMMENTS =====")
        print(f"[DEBUG-SERVICE] Fetching comments for issue ID: {issue_id} in project: {project_id}")

        try:
            # Verify tokens are available before making request
            if not token_store.has_tokens():
                print(f"[DEBUG-SERVICE] Token store is missing tokens, aborting comments request")
                return {"result": 1, "message": "API tokens not available", "data": [], "issueId": issue_id}

            # Step 1: First fetch the issue data to get its UUID
            endpoint = f"project/{project_id}/issue-filter/filter"
            params = {
                "anyFiltersDTO[0][type]": "id",
                "anyFiltersDTO[0][expr]": "1",
                "anyFiltersDTO[0][value][0]": issue_id  # Use the specific issue ID
            }

            # Get issue details to extract UUID
            issue_response = ReviztoAPI.get(endpoint, params)

            # Check if we got a valid response with data
            if (issue_response and
                    issue_response.get('result') == 0 and
                    issue_response.get('data') and
                    issue_response['data'].get('data') and
                    len(issue_response['data']['data']) > 0):

                # Extract the UUID from the issue data for THIS specific issue
                issue_data = issue_response['data']['data'][0]
                issue_uuid = issue_data.get('uuid')

                if issue_uuid:
                    print(f"[DEBUG-SERVICE] Found issue UUID: {issue_uuid}")

                    # Step 2: Now use THIS issue's UUID to fetch comments
                    comments_endpoint = f"issue/{issue_uuid}/comments/date"

                    # Include the required parameters
                    comments_params = {
                        "date": date,
                        "projectId": project_id
                    }

                    # Make API request with the correct parameters
                    comments_response = ReviztoAPI.get(comments_endpoint, comments_params)
                    print(f"[DEBUG-SERVICE] API call successful for comments endpoint")

                    # Check response structure and format
                    if isinstance(comments_response, dict):
                        print(f"[DEBUG-SERVICE] Comments response has keys: {list(comments_response.keys())}")

                        # Make sure we extract the comments data correctly
                        if comments_response.get('result') == 0:
                            comments_data = comments_response.get('data')

                            # Handle different possible formats for the data
                            if comments_data is None:
                                print(f"[DEBUG-SERVICE] Comments data is None")
                                comments_response['data'] = []
                            elif isinstance(comments_data, list):
                                print(f"[DEBUG-SERVICE] Found {len(comments_data)} comments in list format")
                                # Leave as is - already in the correct format
                            elif isinstance(comments_data, dict):
                                print(
                                    f"[DEBUG-SERVICE] Comments data is a dict with keys: {list(comments_data.keys())}")

                                # Try to extract comments from different possible dict structures
                                if 'items' in comments_data and isinstance(comments_data['items'], list):
                                    # Format 1: data = { items: [...comments] }
                                    print(f"[DEBUG-SERVICE] Found {len(comments_data['items'])} comments in data.items")
                                    comments_response['data'] = comments_data['items']
                                elif 'data' in comments_data and isinstance(comments_data['data'], list):
                                    # Format 2: data = { data: [...comments] }
                                    print(f"[DEBUG-SERVICE] Found {len(comments_data['data'])} comments in data.data")
                                    comments_response['data'] = comments_data['data']
                                else:
                                    # If we can't find a list of comments, try using the dict as a single comment
                                    # (rare, but possible for single comments)
                                    if 'type' in comments_data and 'created' in comments_data:
                                        print(f"[DEBUG-SERVICE] Treating dict as a single comment")
                                        comments_response['data'] = [comments_data]
                                    else:
                                        print(f"[DEBUG-SERVICE] Could not identify comments in dict structure")
                                        comments_response['data'] = []
                            else:
                                print(f"[DEBUG-SERVICE] Comments data has unexpected type: {type(comments_data)}")
                                comments_response['data'] = []
                        else:
                            print(
                                f"[DEBUG-SERVICE] Comments response has non-zero result: {comments_response.get('result')}")
                            comments_response['data'] = []
                    else:
                        print(f"[DEBUG-SERVICE] Comments response is not a dict: {type(comments_response)}")
                        comments_response = {"result": 1, "message": "Invalid response format", "data": []}

                    # Add the issue ID to the response for reference on the client side
                    comments_response['issueId'] = issue_id

                    print(f"[DEBUG-SERVICE] ===== END FETCHING ISSUE COMMENTS =====\n")
                    return comments_response
                else:
                    print(f"[DEBUG-SERVICE] Issue found but UUID is missing")
                    return {"result": 1, "message": "Issue UUID not found", "data": [], "issueId": issue_id}
            else:
                print(f"[DEBUG-SERVICE] Issue not found with ID: {issue_id}")
                return {"result": 1, "message": f"Issue not found with ID: {issue_id}", "data": [], "issueId": issue_id}

        except Exception as e:
            print(f"[DEBUG-SERVICE] Error in get_issue_comments: {e}")
            import traceback
            print(f"[DEBUG-SERVICE] Traceback: {traceback.format_exc()}")
            return {"result": 1, "message": str(e), "data": [], "issueId": issue_id}

    @classmethod
    def get_project_workflow_settings(cls, project_id):
        """
        Get workflow settings for a specific project.

        Args:
            project_id (int): Project ID

        Returns:
            dict: Response with workflow settings data
        """
        print(f"[DEBUG] Fetching workflow settings for project ID: {project_id}")
        try:
            # Verify tokens are available before making request
            if not token_store.has_tokens():
                print(f"[DEBUG] Token store is missing tokens, aborting workflow settings request")
                return {"result": 1, "message": "API tokens not available", "data": {}}

            # Use the correct endpoint for workflow settings
            endpoint = "issue-workflow/settings"

            # Make API request
            response = ReviztoAPI.get(endpoint)
            print(f"[DEBUG] Workflow settings API response received: {type(response)}")

            # Return the raw API response
            return response

        except Exception as e:
            import traceback
            print(f"[DEBUG] Failed to get workflow settings: {e}")
            print(f"[DEBUG] Exception traceback: {traceback.format_exc()}")
            return {"result": 1, "message": str(e), "data": {}}