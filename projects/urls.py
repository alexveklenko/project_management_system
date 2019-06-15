from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.index, name='projects'),
    path('<int:id>/', views.project_view, name='project'),
    path('new/', views.new_project, name='new_project'),
    path('<int:id>/edit/', views.edit_project, name='edit_project'),
    path('<int:project_id>/new_task/', views.new_task, name='new_task'),
]
