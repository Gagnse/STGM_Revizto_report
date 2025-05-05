from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/search/', views.get_search_results, name='search_results'),

    # API endpoints for Revizto data
    path('api/projects/<int:project_id>/issues/', views.get_project_issues, name='project_issues'),
    path('api/projects/<int:project_id>/issues/<int:issue_id>/', views.get_issue_details, name='issue_details'),
]