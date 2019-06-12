from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='tasks'),
    path('<int:id>/', views.task_view, name='task'),
    path('new/', views.new_task, name='new_task')
]
