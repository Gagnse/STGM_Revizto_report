from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/search/', views.get_search_results, name='search_results'),

    # API endpoints for Revizto data
    path('api/projects/<int:project_id>/issues/', views.get_project_issues, name='project_issues'),
    path('api/projects/<int:project_id>/issues/<int:issue_id>/', views.get_issue_details, name='issue_details'),
    path('api/projects/<int:project_id>/observations/', views.get_project_observations, name='project_observations'),
    path('api/projects/<int:project_id>/instructions/', views.get_project_instructions, name='project_instructions'),
    path('api/projects/<int:project_id>/deficiencies/', views.get_project_deficiencies, name='project_deficiencies'),
    # API endpoints for project data session storage
    path('api/projects/<int:project_id>/data/save/', views.save_project_data, name='save_project_data'),
    path('api/projects/<int:project_id>/data/load/', views.load_project_data, name='load_project_data'),
    path('api/projects/<int:project_id>/data/clear/', views.clear_project_data, name='clear_project_data'),

    # Debug endpoint for session information
    path('api/debug/session/', views.debug_session, name='debug_session'),
]