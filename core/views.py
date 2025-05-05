from django.shortcuts import render
from django.http import JsonResponse
from .api.service import ReviztoService


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

    # Get matching projects from the API
    projects = ReviztoService.search_projects(query)

    # Convert to serializable format for the dropdown
    results = []
    for project in projects:
        project_id = project.id
        project_name = project.name
        print(f"[DEBUG] Adding result: ID={project_id}, Name={project_name}")
        results.append({
            'id': project_id,
            'text': project_name
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