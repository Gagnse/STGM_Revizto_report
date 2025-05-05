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
    This is just a placeholder that returns mock data
    """
    query = request.GET.get('query', '')

    # Mock search results
    results = [
        {'id': 1, 'text': f'Result for {query} - Item 1'},
        {'id': 2, 'text': f'Result for {query} - Item 2'},
        {'id': 3, 'text': f'Result for {query} - Item 3'}
    ]

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