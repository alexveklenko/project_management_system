from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='projects'),
    path('<int:id>/', views.project_view, name='project'),
    path('new/', views.new_project, name='new_project'),
    path('<int:id>/edit/', views.edit_project, name='edit_project'),
]
