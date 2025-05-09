import logging
from .client import ReviztoAPI
from .models import Project, Issue, User

logger = logging.getLogger(__name__)


class ReviztoService:
    """Service for retrieving data from the Revizto API."""

    @classmethod
    def get_projects(cls):
        """Get a list of all projects."""
        print("\n[DEBUG] ==== STARTING GET_PROJECTS ====")
        try:
            if not ReviztoAPI.LICENCE_UUID:
                print("[DEBUG] REVIZTO_LICENCE_UUID is not set in settings")
                return []

            print(f"[DEBUG] Using license UUID: {ReviztoAPI.LICENCE_UUID}")

            # Use the correct endpoint format for Revizto API
            # Format: project/list/{licenceUUID}/paged
            endpoint = f"project/list/{ReviztoAPI.LICENCE_UUID}/paged"
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

                # Check for successful response
                if data.get('result') == 0 and 'data' in data:
                    print(f"[DEBUG] Successfully received project data")

                    # Navigate through the response structure based on the actual API response
                    # The specific path depends on the Revizto API response format
                    projects_data = data.get('data', {}).get('items', [])

                    if isinstance(projects_data, list):
                        print(f"[DEBUG] Found {len(projects_data)} projects in the response")

                        for project_data in projects_data:
                            print(f"[DEBUG] Processing project with ID: {project_data.get('id')}")
                            projects.append(Project(project_data))
                    else:
                        print(f"[DEBUG] Projects data not in expected list format: {type(projects_data)}")
                else:
                    print(f"[DEBUG] API error: {data.get('message', 'Unknown error')}")

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
                "reportSort[2][field]": "sheet",
                "reportSort[2][direction]": "asc",
                "reportSort[3][field]": "id",
                "reportSort[3][direction]": "asc",
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

    @classmethod
    def get_issue_comments(cls, project_id, issue_id, date):
        """Get comments history for a specific issue."""
        print(f"\n[DEBUG-SERVICE] ===== FETCHING ISSUE COMMENTS =====")
        print(f"[DEBUG-SERVICE] Fetching comments for issue ID: {issue_id} in project: {project_id}")

        try:
            # Step 1: First we need to fetch the issue data to get its UUID
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
                    print(f"[DEBUG-SERVICE] API call successful")

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
