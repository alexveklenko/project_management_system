from django.shortcuts import render

from .models import Task


def index(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/index.html', {'tasks': tasks})


def task_view(request, id):
    task = Task.objects.get(id=id)
    return render(request, 'tasks/single_task.html', {'task': task})
