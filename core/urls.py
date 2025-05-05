from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/search/', views.get_search_results, name='search_results'),
]