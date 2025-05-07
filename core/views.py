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