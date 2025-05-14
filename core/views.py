from django.shortcuts import render
from django.http import JsonResponse

from DjangoProject import settings
from .api.client import ReviztoAPI
from .api.service import ReviztoService
import json
import logging
from datetime import datetime
from .models import ProjectData

# Set up logger
logger = logging.getLogger(__name__)


def home_view(request):
    """
    View for the home page that renders the index.html template
    """
    # Get projects from the API
    projects = ReviztoService.get_projects()

    # Pass data to the template
    context = {
        'projects': projects
    }

    return render(request, 'index.html', context)


def get_search_results(request):
    """
    API endpoint to get search results for the dropdown
    Searches projects by title
    """
    query = request.GET.get('query', '')
    print(f"[DEBUG] Search request received with query: '{query}'")
    logger.info("Search request with query: %s", query)

    # Get matching projects from the API
    projects = ReviztoService.search_projects(query)

    # Convert to serializable format for the dropdown
    results = []
    for project in projects:
        project_id = project.id
        project_name = project.name
        print(f"[DEBUG] Adding result: ID={project_id}, Name={project_name}")

        # Check if this project has saved data in the database
        has_saved_data = ProjectData.objects.filter(id=project_id).exists()

        print(f"[DEBUG] Project {project_id} has saved data: {has_saved_data}")

        results.append({
            'id': project_id,
            'text': project_name,
            'hasSavedData': has_saved_data
        })

    print(f"[DEBUG] Returning {len(results)} search results")
    return JsonResponse({'results': results})


def get_project_issues(request, project_id):
    """
    API endpoint to get issues for a specific project
    """
    status = request.GET.get('status', None)

    # Get issues from the API
    issues = ReviztoService.get_issues(project_id, status=status)

    # Convert to serializable format
    serialized_issues = [issue.raw_data for issue in issues]

    return JsonResponse({'issues': serialized_issues})


def get_issue_details(request, project_id, issue_id):
    """
    API endpoint to get details for a specific issue
    """
    # Get issue from the API
    issue = ReviztoService.get_issue(project_id, issue_id)

    if not issue:
        return JsonResponse({'error': 'Issue not found'}, status=404)

    return JsonResponse(issue.raw_data)


def save_project_data(request, project_id):
    """
    API endpoint to save project form data to database
    Creates new entry if project doesn't exist, otherwise updates existing entry
    """
    if request.method != 'POST':
        logger.warning("Save project data called with non-POST method: %s", request.method)
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    try:
        # Get data from POST request
        data = json.loads(request.body)

        # Debug request and data
        print(f"[DEBUG] Saving data for project {project_id}")
        print(f"[DEBUG] Data keys: {list(data.keys())}")

        # Format dates if they exist
        report_date = None
        if data.get('reportDate'):
            try:
                report_date = datetime.strptime(data['reportDate'], '%Y-%m-%d')
            except ValueError:
                # Try alternative format
                try:
                    report_date = datetime.strptime(data['reportDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                except ValueError:
                    logger.warning(f"Could not parse report date: {data['reportDate']}")

        visit_date = None
        if data.get('visitDate'):
            try:
                visit_date = datetime.strptime(data['visitDate'], '%Y-%m-%d')
            except ValueError:
                # Try alternative format
                try:
                    visit_date = datetime.strptime(data['visitDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                except ValueError:
                    logger.warning(f"Could not parse visit date: {data['visitDate']}")

        # Try to get existing project data or create new entry
        try:
            project_data = ProjectData.objects.get(id=project_id)
            created = False
        except ProjectData.DoesNotExist:
            project_data = ProjectData(id=project_id)
            created = True

        # Update the fields using the correct lowercase field names
        project_data.nodossier = data.get('architectFile', '')
        project_data.noprojet = data.get('projectName', '')
        project_data.maitreouvragge = data.get('projectOwner', '')
        project_data.entrepreneur = data.get('contractor', '')
        project_data.novisite = data.get('visitNumber', '')
        project_data.visitepar = data.get('visitBy', '')
        project_data.datevisite = visit_date
        project_data.presence = data.get('inPresenceOf', '')
        project_data.rapportdate = report_date
        project_data.description = data.get('description', '')
        project_data.distribution = data.get('distribution', '')
        project_data.image = data.get('imageUrl', '')

        # Save the updated or new record
        project_data.save()

        logger.info("Project %s data saved to database. Created: %s", project_id, created)

        return JsonResponse({
            'success': True,
            'message': 'Data saved successfully to database',
            'created': created
        })

    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in request body: {str(e)}"
        print(f"[DEBUG] {error_msg}")
        logger.error(error_msg)
        return JsonResponse({'error': error_msg}, status=400)

    except Exception as e:
        error_msg = f"Error saving project data: {str(e)}"
        print(f"[DEBUG] {error_msg}")
        logger.error(error_msg, exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)

def load_project_data(request, project_id):
    """
    API endpoint to load project form data from database
    """
    # Debug state
    print(f"[DEBUG] Loading data for project {project_id}")

    try:
        # Try to get project data from database
        project_exists = ProjectData.objects.filter(id=project_id).exists()

        if project_exists:
            project_data = ProjectData.objects.get(id=project_id)

            # Format dates for JSON
            report_date = ''
            if project_data.rapportdate:
                report_date = project_data.rapportdate.strftime('%Y-%m-%d')

            visit_date = ''
            if project_data.datevisite:
                visit_date = project_data.datevisite.strftime('%Y-%m-%d')

            # Convert to response format - map the lowercase DB columns back to camelCase for frontend
            data = {
                'architectFile': project_data.nodossier or '',
                'projectName': project_data.noprojet or '',
                'projectOwner': project_data.maitreouvragge or '',
                'contractor': project_data.entrepreneur or '',
                'visitNumber': project_data.novisite or '',
                'visitBy': project_data.visitepar or '',
                'visitDate': visit_date,
                'inPresenceOf': project_data.presence or '',
                'reportDate': report_date,
                'description': project_data.description or '',
                'distribution': project_data.distribution or '',
                'imageUrl': project_data.image or '',
                'lastSaved': datetime.now().isoformat()
            }

            print(f"[DEBUG] Loaded project data with keys: {list(data.keys())}")
            logger.info("Loaded project data for project %s", project_id)

            return JsonResponse({
                'success': True,
                'data': data,
                'has_data': True
            })
        else:
            print(f"[DEBUG] No saved data found for project {project_id}")
            logger.info("No saved data found for project %s", project_id)

            return JsonResponse({
                'success': True,
                'data': {},
                'has_data': False
            })

    except Exception as e:
        error_msg = f"Error loading project data: {str(e)}"
        print(f"[DEBUG] {error_msg}")
        logger.error(error_msg, exc_info=True)
        return JsonResponse({'error': str(e), 'success': False}, status=500)

def clear_project_data(request, project_id):
    """
    API endpoint to clear project form data from database
    """
    if request.method != 'POST':
        logger.warning("Clear project data called with non-POST method: %s", request.method)
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    # Debug state
    print(f"[DEBUG] Clearing data for project {project_id}")

    try:
        # Remove project data from database
        deleted, _ = ProjectData.objects.filter(id=project_id).delete()

        if deleted:
            print(f"[DEBUG] Removed data for project {project_id} from database")
            logger.info("Removed data for project %s from database", project_id)
            return JsonResponse({
                'success': True,
                'message': 'Data cleared successfully from database',
                'removed': True
            })
        else:
            print(f"[DEBUG] No data found for project {project_id} to clear")
            logger.info("No data found for project %s to clear", project_id)
            return JsonResponse({
                'success': True,
                'message': 'No data found to clear',
                'removed': False
            })

    except Exception as e:
        error_msg = f"Error clearing project data: {str(e)}"
        print(f"[DEBUG] {error_msg}")
        logger.error(error_msg, exc_info=True)
        return JsonResponse({'error': str(e), 'success': False}, status=500)


def debug_session(request):
    """
    Debug endpoint that returns basic debug info
    """
    print("\n=== DEBUG SESSION INFO ===")
    print(f"Session key: {request.session.session_key}")
    print("=========================\n")

    return JsonResponse({
        'success': True,
        'message': 'Debug info printed to console'
    })


def get_project_observations(request, project_id):
    """
    API endpoint to get observations for a specific project
    """
    print(f"[DEBUG] Observations request received for project ID: {project_id}")

    # Get observations from the API
    response_data = ReviztoService.get_observations(project_id)

    # Return the raw API response
    return JsonResponse(response_data)


def get_project_instructions(request, project_id):
    """
    API endpoint to get instructions for a specific project
    """
    print(f"[DEBUG] Instructions request received for project ID: {project_id}")

    # Get instructions from the API
    response_data = ReviztoService.get_instructions(project_id)

    # Return the raw API response
    return JsonResponse(response_data)


def get_project_deficiencies(request, project_id):
    """
    API endpoint to get deficiencies for a specific project
    """
    print(f"\n\n[DEBUG-SERVER] ===== DEFICIENCIES REQUEST =====")
    print(f"[DEBUG-SERVER] Deficiencies request received for project ID: {project_id}")

    try:
        # Get deficiencies from the API
        print(f"[DEBUG-SERVER] Calling ReviztoService.get_deficiencies for project ID: {project_id}")
        response_data = ReviztoService.get_deficiencies(project_id)

        # Debug the response structure
        print(f"[DEBUG-SERVER] Response data type: {type(response_data)}")
        if isinstance(response_data, dict):
            print(f"[DEBUG-SERVER] Response keys: {list(response_data.keys())}")

            # Check result key
            if 'result' in response_data:
                print(f"[DEBUG-SERVER] Result value: {response_data['result']}")

            # Check data structure
            if 'data' in response_data and isinstance(response_data['data'], dict):
                print(f"[DEBUG-SERVER] Data keys: {list(response_data['data'].keys())}")

                if 'data' in response_data['data']:
                    data_list = response_data['data']['data']
                    print(f"[DEBUG-SERVER] Items in data.data: {len(data_list)}")

                    # Debug first item if available
                    if len(data_list) > 0:
                        first_item = data_list[0]
                        print(f"[DEBUG-SERVER] First item ID: {first_item.get('id')}")
                        print(f"[DEBUG-SERVER] First item keys: {list(first_item.keys())[:10]}...")

        print(f"[DEBUG-SERVER] ===== END DEFICIENCIES REQUEST =====\n\n")

        # Return the raw API response
        return JsonResponse(response_data)

    except Exception as e:
        print(f"[DEBUG-SERVER] Error in get_project_deficiencies: {e}")
        import traceback
        print(f"[DEBUG-SERVER] Traceback: {traceback.format_exc()}")
        return JsonResponse({"result": 1, "message": str(e), "data": {"data": []}})


def get_project_workflow_settings(request, project_id):
    """
    API endpoint to get workflow settings for a project.
    This includes custom statuses, types, and workflows.
    """
    print(f"\n[DEBUG] ===== WORKFLOW SETTINGS REQUEST =====")
    print(f"[DEBUG] Workflow settings request received for project ID: {project_id}")

    try:
        # Create endpoint URL using project ID - IMPORTANT: Using the correct endpoint format
        # The endpoint should be 'issue-workflow/settings' not 'project/{project_id}/issue-workflow/settings'
        endpoint = f"issue-workflow/settings"
        print(f"[DEBUG] Using endpoint: {endpoint}")

        # Make API request
        try:
            response_data = ReviztoAPI.get(endpoint)
            print(f"[DEBUG] Workflow settings response received with status:{response_data.get('result')}")

            # Debug the response data
            if isinstance(response_data, dict):
                print(f"[DEBUG] Response keys: {list(response_data.keys())}")

                if response_data.get('result') == 0 and 'data' in response_data:
                    data = response_data['data']
                    print(f"[DEBUG] Data keys: {list(data.keys())}")

                    # Debug statuses specifically
                    if 'statuses' in data:
                        statuses = data['statuses']
                        print(f"[DEBUG] Found {len(statuses)} statuses")

                        # Print first few statuses
                        for i, status in enumerate(statuses[:3]):
                            print(f"[DEBUG] Status {i + 1}: {status.get('name')} - UUID: {status.get('uuid')}")
                else:
                    print(f"[DEBUG] Error in response: {response_data.get('message', 'No message')}")
            else:
                print(f"[DEBUG] Response data is not a dictionary: {type(response_data)}")

        except Exception as api_error:
            print(f"[DEBUG] API request failed: {api_error}")
            import traceback
            print(f"[DEBUG] API error traceback: {traceback.format_exc()}")
            response_data = {"result": 1, "message": str(api_error), "data": {}}

        # Return the raw API response
        return JsonResponse(response_data)
    except Exception as e:
        print(f"[DEBUG] Error in get_project_workflow_settings: {e}")
        import traceback
        print(f"[DEBUG] Traceback: {traceback.format_exc()}")
        return JsonResponse({"result": 1, "message": str(e), "data": {}})


def get_issue_comments(request, project_id, issue_id):
    """
    API endpoint to get comments/history for a specific issue
    """
    print(f"[DEBUG] Fetching comments for issue ID: {issue_id} in project: {project_id}")

    # Get date parameter with default to "2018-05-30" (as in your current code)
    date_param = request.GET.get('date', '2018-05-30')

    try:
        # Get comments from the API via service
        response_data = ReviztoService.get_issue_comments(project_id, issue_id, date_param)

        # Ensure a consistent response structure
        if response_data.get('result') == 0:
            # Extract comments array from potential nested structure
            comments_data = response_data.get('data', [])

            if isinstance(comments_data, dict) and 'data' in comments_data:
                # If data is nested one level down in data.data
                response_data['data'] = comments_data.get('data', [])
            elif isinstance(comments_data, dict) and 'items' in comments_data:
                # If data is in data.items
                response_data['data'] = comments_data.get('items', [])
            # Keep as is if it's already the expected array format

        # Return the normalized API response
        return JsonResponse(response_data)
    except Exception as e:
        print(f"[DEBUG] Error in get_issue_comments: {e}")
        import traceback
        print(f"[DEBUG] Traceback: {traceback.format_exc()}")
        return JsonResponse({"result": 1, "message": str(e), "data": []})

def generate_pdf(request, project_id):
    """
    Generate a PDF report for the project
    """
    print(f"[DEBUG] PDF generation requested for project: {project_id}")

    try:
        # Get project data from the database
        project_data = ProjectData.objects.filter(id=project_id).first()

        if not project_data:
            print(f"[DEBUG] No project data found for project ID: {project_id}")
            return JsonResponse({'error': 'Project data not found'}, status=404)

        # Convert ProjectData to a dictionary format similar to what would be returned by load_project_data
        report_date = ''
        if project_data.rapportDate:
            report_date = project_data.rapportDate.strftime('%Y-%m-%d')

        visit_date = ''
        if project_data.dateVisite:
            visit_date = project_data.dateVisite.strftime('%Y-%m-%d')

        project_info = {
            'architectFile': project_data.noDossier or '',
            'projectName': project_data.noProjet or '',
            'projectOwner': project_data.maitreOuvragge or '',
            'contractor': project_data.entrepreneur or '',
            'visitNumber': project_data.noVisite or '',
            'visitBy': project_data.visitePar or '',
            'visitDate': visit_date,
            'inPresenceOf': project_data.presence or '',
            'reportDate': report_date,
            'description': project_data.description or '',
            'distribution': project_data.distribution or '',
            'imageUrl': project_data.image or '',
        }

        # Get observations, instructions, and deficiencies from the API
        observations = []
        instructions = []
        deficiencies = []
        issue_comments = {}  # Dictionary to store comments for each issue

        # Get observations
        observations_response = ReviztoService.get_observations(project_id)
        if observations_response and observations_response.get('result') == 0 and observations_response.get('data') and \
                observations_response['data'].get('data'):
            observations = observations_response['data']['data']
            print(f"[DEBUG] Found {len(observations)} observations")

            # Fetch comments for each observation
            for obs in observations:
                if obs.get('id'):
                    # Use a fixed date in the past to ensure we get all comments
                    comments_response = ReviztoService.get_issue_comments(project_id, obs['id'], '2018-05-30')
                    if comments_response and comments_response.get('result') == 0:
                        # Extract the comments data properly
                        comments_data = comments_response.get('data', [])
                        # Critical fix: Handle both list and dict formats for comments
                        if isinstance(comments_data, list):
                            # Already a list, use as-is
                            issue_comments[str(obs['id'])] = comments_data
                            print(f"[DEBUG] Found {len(comments_data)} comments for observation {obs['id']}")
                        elif isinstance(comments_data, dict):
                            # Convert dict to list if it has items
                            # This is a critical fix for when API returns object instead of array
                            print(f"[DEBUG] Comments data for observation {obs['id']} is a dict with keys: {list(comments_data.keys())}")
                            if 'items' in comments_data and isinstance(comments_data['items'], list):
                                issue_comments[str(obs['id'])] = comments_data['items']
                                print(f"[DEBUG] Extracted {len(comments_data['items'])} comments from dict for observation {obs['id']}")
                            else:
                                # If no items found, create empty list
                                issue_comments[str(obs['id'])] = []
                        else:
                            print(f"[DEBUG] Comments data for observation {obs['id']} is not a list or dict: {type(comments_data)}")
                            issue_comments[str(obs['id'])] = []
                    else:
                        print(f"[DEBUG] Failed to get comments for observation {obs['id']}")
                        issue_comments[str(obs['id'])] = []

        # Get instructions
        instructions_response = ReviztoService.get_instructions(project_id)
        if instructions_response and instructions_response.get('result') == 0 and instructions_response.get('data') and \
                instructions_response['data'].get('data'):
            instructions = instructions_response['data']['data']
            print(f"[DEBUG] Found {len(instructions)} instructions")

            # Fetch comments for each instruction
            for ins in instructions:
                if ins.get('id'):
                    # Use a fixed date in the past to ensure we get all comments
                    comments_response = ReviztoService.get_issue_comments(project_id, ins['id'], '2018-05-30')
                    if comments_response and comments_response.get('result') == 0:
                        # Extract the comments data properly
                        comments_data = comments_response.get('data', [])
                        # Critical fix: Handle both list and dict formats for comments
                        if isinstance(comments_data, list):
                            # Already a list, use as-is
                            issue_comments[str(ins['id'])] = comments_data
                            print(f"[DEBUG] Found {len(comments_data)} comments for instruction {ins['id']}")
                        elif isinstance(comments_data, dict):
                            # Convert dict to list if it has items
                            print(f"[DEBUG] Comments data for instruction {ins['id']} is a dict with keys: {list(comments_data.keys())}")
                            if 'items' in comments_data and isinstance(comments_data['items'], list):
                                issue_comments[str(ins['id'])] = comments_data['items']
                                print(f"[DEBUG] Extracted {len(comments_data['items'])} comments from dict for instruction {ins['id']}")
                            else:
                                # If no items found, create empty list
                                issue_comments[str(ins['id'])] = []
                        else:
                            print(f"[DEBUG] Comments data for instruction {ins['id']} is not a list or dict: {type(comments_data)}")
                            issue_comments[str(ins['id'])] = []
                    else:
                        print(f"[DEBUG] Failed to get comments for instruction {ins['id']}")
                        issue_comments[str(ins['id'])] = []

        # Get deficiencies
        deficiencies_response = ReviztoService.get_deficiencies(project_id)
        if deficiencies_response and deficiencies_response.get('result') == 0 and deficiencies_response.get('data') and \
                deficiencies_response['data'].get('data'):
            deficiencies = deficiencies_response['data']['data']
            print(f"[DEBUG] Found {len(deficiencies)} deficiencies")

            # Fetch comments for each deficiency
            for def_item in deficiencies:
                if def_item.get('id'):
                    # Use a fixed date in the past to ensure we get all comments
                    comments_response = ReviztoService.get_issue_comments(project_id, def_item['id'], '2018-05-30')
                    if comments_response and comments_response.get('result') == 0:
                        # Extract the comments data properly
                        comments_data = comments_response.get('data', [])
                        # Critical fix: Handle both list and dict formats for comments
                        if isinstance(comments_data, list):
                            # Already a list, use as-is
                            issue_comments[str(def_item['id'])] = comments_data
                            print(f"[DEBUG] Found {len(comments_data)} comments for deficiency {def_item['id']}")
                        elif isinstance(comments_data, dict):
                            # Convert dict to list if it has items
                            print(f"[DEBUG] Comments data for deficiency {def_item['id']} is a dict with keys: {list(comments_data.keys())}")
                            if 'items' in comments_data and isinstance(comments_data['items'], list):
                                issue_comments[str(def_item['id'])] = comments_data['items']
                                print(f"[DEBUG] Extracted {len(comments_data['items'])} comments from dict for deficiency {def_item['id']}")
                            else:
                                # If no items found, create empty list
                                issue_comments[str(def_item['id'])] = []
                        else:
                            print(f"[DEBUG] Comments data for deficiency {def_item['id']} is not a list or dict: {type(comments_data)}")
                            issue_comments[str(def_item['id'])] = []
                    else:
                        print(f"[DEBUG] Failed to get comments for deficiency {def_item['id']}")
                        issue_comments[str(def_item['id'])] = []

        # Debug the issue_comments dictionary
        print(f"[DEBUG] Total issues with comments: {len(issue_comments)}")
        for issue_id, comments in issue_comments.items():
            print(f"[DEBUG] Issue {issue_id} has {len(comments)} comments")
            if len(comments) > 0:
                print(f"[DEBUG] First comment type: {type(comments[0])}")
                if isinstance(comments[0], dict):
                    print(f"[DEBUG] First comment keys: {list(comments[0].keys())}")

        # Import the PDF generator
        from .pdf_generator import generate_report_pdf

        # Generate PDF with comments
        print(f"[DEBUG] Generating PDF with {len(observations)} observations, {len(instructions)} instructions, {len(deficiencies)} deficiencies, and comments for {len(issue_comments)} issues")
        pdf_buffer = generate_report_pdf(project_id, project_info, observations, instructions, deficiencies, issue_comments)

        # Create a response with PDF content
        from django.http import HttpResponse
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')

        # Set filename
        project_name = project_info['projectName'] or f"Projet_{project_id}"
        project_name = project_name.replace(' ', '_')

        response['Content-Disposition'] = f'attachment; filename="Rapport_Visite_{project_name}.pdf"'

        print(f"[DEBUG] PDF successfully generated for project {project_id}")
        return response

    except Exception as e:
        import traceback
        print(f"[DEBUG] Error generating PDF: {e}")
        print(f"[DEBUG] Traceback: {traceback.format_exc()}")
        return JsonResponse({'error': str(e)}, status=500)

def debug_token_state(request):
    """
    Debug endpoint that shows the current token state (without revealing the tokens)
    """
    from .api.client import ReviztoAPI
    from datetime import datetime

    # Get token state
    token_state = {
        'access_token_exists': bool(ReviztoAPI.ACCESS_TOKEN),
        'access_token_length': len(ReviztoAPI.ACCESS_TOKEN) if ReviztoAPI.ACCESS_TOKEN else 0,
        'access_token_prefix': ReviztoAPI.ACCESS_TOKEN[:10] + '...' if ReviztoAPI.ACCESS_TOKEN and len(
            ReviztoAPI.ACCESS_TOKEN) > 10 else None,

        'refresh_token_exists': bool(ReviztoAPI.REFRESH_TOKEN),
        'refresh_token_length': len(ReviztoAPI.REFRESH_TOKEN) if ReviztoAPI.REFRESH_TOKEN else 0,
        'refresh_token_prefix': ReviztoAPI.REFRESH_TOKEN[:10] + '...' if ReviztoAPI.REFRESH_TOKEN and len(
            ReviztoAPI.REFRESH_TOKEN) > 10 else None,

        'token_expiry': str(ReviztoAPI.TOKEN_EXPIRY) if ReviztoAPI.TOKEN_EXPIRY else None,
        'is_expired': ReviztoAPI.TOKEN_EXPIRY < datetime.now() if ReviztoAPI.TOKEN_EXPIRY else True,
        'time_until_expiry': str(
            ReviztoAPI.TOKEN_EXPIRY - datetime.now()) if ReviztoAPI.TOKEN_EXPIRY and ReviztoAPI.TOKEN_EXPIRY > datetime.now() else 'Expired',

        'licence_uuid_exists': bool(ReviztoAPI.LICENCE_UUID),
        'licence_uuid_length': len(ReviztoAPI.LICENCE_UUID) if ReviztoAPI.LICENCE_UUID else 0,
        'licence_uuid_preview': ReviztoAPI.LICENCE_UUID[:8] + '...' if ReviztoAPI.LICENCE_UUID and len(
            ReviztoAPI.LICENCE_UUID) > 8 else ReviztoAPI.LICENCE_UUID,
    }

    # Test token validity
    try:
        token_state['token_validity_check'] = ReviztoAPI.ensure_token_valid()
    except Exception as e:
        token_state['token_validity_check'] = False
        token_state['token_validity_error'] = str(e)

    # Environment info
    from django.conf import settings
    env_info = {
        'REVIZTO_ENABLE_TOKEN_REFRESH': getattr(settings, 'REVIZTO_ENABLE_TOKEN_REFRESH', None),
        'REVIZTO_API_BASE_URL': getattr(settings, 'REVIZTO_API_BASE_URL', None),
        'settings_access_token_length': len(getattr(settings, 'REVIZTO_ACCESS_TOKEN', '')),
        'settings_refresh_token_length': len(getattr(settings, 'REVIZTO_REFRESH_TOKEN', '')),
        'settings_licence_uuid_length': len(getattr(settings, 'REVIZTO_LICENCE_UUID', '')),
        'running_on_heroku': bool(os.environ.get('DYNO')),
    }

    return JsonResponse({
        'token_state': token_state,
        'environment': env_info,
        'current_time': str(datetime.now())
    })

print(f"Access Token available: {'YES' if settings.REVIZTO_ACCESS_TOKEN else 'NO'}")
print(f"Refresh Token available: {'YES' if settings.REVIZTO_REFRESH_TOKEN else 'NO'}")
print(f"License UUID available: {'YES' if settings.REVIZTO_LICENCE_UUID else 'NO'}")


def check_token_state(request):
    """Check the current state of API tokens."""
    from .api import token_store

    token_state = {
        'access_token_exists': bool(token_store.get_access_token()),
        'access_token_length': len(token_store.get_access_token() or ''),
        'refresh_token_exists': bool(token_store.get_refresh_token()),
        'refresh_token_length': len(token_store.get_refresh_token() or ''),
        'licence_uuid_exists': bool(token_store.get_licence_uuid()),
        'licence_uuid_length': len(token_store.get_licence_uuid() or ''),
        'token_expiry': str(token_store.get_token_expiry()),
    }

    return JsonResponse(token_state)