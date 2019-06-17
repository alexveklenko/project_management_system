from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.index, name='tasks'),
    path('<int:id>/', views.task_view, name='task'),
    path('<int:id>/edit/', views.edit_task, name='edit_task'),
    path('<int:id>/log_time/', views.log_time, name='log_time'),
    path('new/', views.new_task, name='new_task'),
    path('ajax/', views.ajax_get_members, name='ajax_get_members'),
]
