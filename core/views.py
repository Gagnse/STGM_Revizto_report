from django.shortcuts import render
from django.http import JsonResponse
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
        project_data, created = ProjectData.objects.get_or_create(
            id=project_id,
            defaults={
                'noDossier': data.get('architectFile', ''),
                'noProjet': data.get('projectName', ''),
                'maitreOuvragge': data.get('projectOwner', ''),
                'entrepreneur': data.get('contractor', ''),
                'noVisite': data.get('visitNumber', ''),
                'visitePar': data.get('visitBy', ''),
                'dateVisite': visit_date,
                'presence': data.get('inPresenceOf', ''),
                'rapportDate': report_date,
                'description': data.get('description', ''),
                'distribution': data.get('distribution', ''),
                'image': data.get('imageUrl', '')
            }
        )

        if not created:
            # Update existing project data
            project_data.noDossier = data.get('architectFile', '')
            project_data.noProjet = data.get('projectName', '')
            project_data.maitreOuvragge = data.get('projectOwner', '')
            project_data.entrepreneur = data.get('contractor', '')
            project_data.noVisite = data.get('visitNumber', '')
            project_data.visitePar = data.get('visitBy', '')
            project_data.dateVisite = visit_date
            project_data.presence = data.get('inPresenceOf', '')
            project_data.rapportDate = report_date
            project_data.description = data.get('description', '')
            project_data.distribution = data.get('distribution', '')
            project_data.image = data.get('imageUrl', '')
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
            if project_data.rapportDate:
                report_date = project_data.rapportDate.strftime('%Y-%m-%d')

            visit_date = ''
            if project_data.dateVisite:
                visit_date = project_data.dateVisite.strftime('%Y-%m-%d')

            # Convert to response format
            data = {
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

    # Get date parameter with default to empty string (which will fetch all comments)
    date_param = request.GET.get('date', '2018-05-30')

    try:
        # Get comments from the API via service
        response_data = ReviztoService.get_issue_comments(project_id, issue_id, date_param)

        # Return the raw API response
        return JsonResponse(response_data)
    except Exception as e:
        print(f"[DEBUG] Error in get_issue_comments: {e}")
        import traceback
        print(f"[DEBUG] Traceback: {traceback.format_exc()}")
        return JsonResponse({"result": 1, "message": str(e), "data": []})