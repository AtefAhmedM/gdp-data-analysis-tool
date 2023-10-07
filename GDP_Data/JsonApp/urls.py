from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('filter/', views.filter_data, name='filter_data'),
    # Add other URL patterns as needed
]
