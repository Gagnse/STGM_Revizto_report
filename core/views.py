from django.shortcuts import render
from django.http import JsonResponse


def home_view(request):
    """
    View for the home page that renders the index.html template
    """
    return render(request, 'index.html')


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