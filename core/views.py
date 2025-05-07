from django.shortcuts import render
from django.http import JsonResponse
from .api.service import ReviztoService
import json
import logging

# Set up logger
logger = logging.getLogger(__name__)


def home_view(request):
    """
    View for the home page that renders the index.html template
    """
    # Debug session state
    logger.info("Session ID: %s", request.session.session_key)
    logger.info("Session keys: %s", list(request.session.keys()))

    print(f"[DEBUG] Session ID: {request.session.session_key}")
    print(f"[DEBUG] Session keys: {list(request.session.keys())}")

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

    # Debug session state
    print(f"[DEBUG] Session ID: {request.session.session_key}")
    print(f"[DEBUG] Session keys: {list(request.session.keys())}")
    logger.info("Session keys during search: %s", list(request.session.keys()))

    # Convert to serializable format for the dropdown
    results = []
    for project in projects:
        project_id = project.id
        project_name = project.name
        print(f"[DEBUG] Adding result: ID={project_id}, Name={project_name}")

        # Check if this project has saved data in the session
        project_session_key = f"project_{project_id}_data"
        has_saved_data = project_session_key in request.session

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
    API endpoint to save project form data to session
    """
    if request.method != 'POST':
        logger.warning("Save project data called with non-POST method: %s", request.method)
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    try:
        # Get data from POST request
        data = json.loads(request.body)

        # Debug request and data
        print(f"[DEBUG] Saving data for project {project_id}")
        print(f"[DEBUG] Session ID: {request.session.session_key}")
        print(f"[DEBUG] CSRF Token: {request.META.get('CSRF_COOKIE', 'Not found')}")
        print(f"[DEBUG] Data keys: {list(data.keys())}")

        logger.info("Saving data for project %s with session ID %s",
                    project_id, request.session.session_key)

        # Ensure a session exists
        if not request.session.session_key:
            request.session.create()
            print(f"[DEBUG] Created new session with ID: {request.session.session_key}")
            logger.info("Created new session with ID: %s", request.session.session_key)

        # Store in session with project-specific key
        session_key = f"project_{project_id}_data"
        request.session[session_key] = data

        # Force save the session
        request.session.modified = True

        # Debug session after save
        print(f"[DEBUG] Session keys after save: {list(request.session.keys())}")
        print(f"[DEBUG] Project data saved to session with key: {session_key}")

        logger.info("Project %s data saved to session. Keys: %s",
                    project_id, list(request.session.keys()))

        return JsonResponse({
            'success': True,
            'message': 'Data saved successfully',
            'sessionId': request.session.session_key,
            'sessionKeys': list(request.session.keys())
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
    API endpoint to load project form data from session
    """
    # Debug session state
    print(f"[DEBUG] Loading data for project {project_id}")
    print(f"[DEBUG] Session ID: {request.session.session_key}")
    print(f"[DEBUG] Session keys: {list(request.session.keys())}")

    logger.info("Loading data for project %s. Session keys: %s",
                project_id, list(request.session.keys()))

    # Get project data from session
    session_key = f"project_{project_id}_data"
    has_data = session_key in request.session

    print(f"[DEBUG] Session key '{session_key}' exists: {has_data}")

    if has_data:
        project_data = request.session[session_key]
        print(f"[DEBUG] Loaded project data with keys: {list(project_data.keys())}")
        logger.info("Loaded project data for project %s", project_id)
    else:
        project_data = {}
        print(f"[DEBUG] No saved data found for project {project_id}")
        logger.info("No saved data found for project %s", project_id)

    return JsonResponse({
        'success': True,
        'data': project_data,
        'has_data': bool(project_data),
        'session_debug': {
            'sessionId': request.session.session_key,
            'sessionKeys': list(request.session.keys())
        }
    })


def clear_project_data(request, project_id):
    """
    API endpoint to clear project form data from session
    """
    if request.method != 'POST':
        logger.warning("Clear project data called with non-POST method: %s", request.method)
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    # Debug session state
    print(f"[DEBUG] Clearing data for project {project_id}")
    print(f"[DEBUG] Session ID: {request.session.session_key}")
    print(f"[DEBUG] Session keys before clear: {list(request.session.keys())}")

    logger.info("Clearing data for project %s. Session keys before: %s",
                project_id, list(request.session.keys()))

    # Remove project data from session
    session_key = f"project_{project_id}_data"
    removed = False

    if session_key in request.session:
        del request.session[session_key]
        request.session.modified = True
        removed = True
        print(f"[DEBUG] Removed data for project {project_id} from session")
        logger.info("Removed data for project %s from session", project_id)
    else:
        print(f"[DEBUG] No data found for project {project_id} to clear")
        logger.info("No data found for project %s to clear", project_id)

    # Debug session after clear
    print(f"[DEBUG] Session keys after clear: {list(request.session.keys())}")

    return JsonResponse({
        'success': True,
        'message': 'Data cleared successfully',
        'removed': removed,
        'sessionId': request.session.session_key,
        'sessionKeys': list(request.session.keys())
    })


def debug_session(request):
    """
    Debug endpoint to view session information
    """
    if not request.session.session_key:
        request.session.create()

    session_data = {
        'session_key': request.session.session_key,
        'session_items': {k: request.session[k] for k in request.session.keys()},
        'cookie_age': request.session.get_expiry_age(),
        'expire_date': request.session.get_expiry_date().isoformat()
    }

    print(f"[DEBUG] Session debug info: {session_data}")
    logger.info("Session debug info: %s", session_data)

    return JsonResponse({
        'success': True,
        'session_data': session_data
    })