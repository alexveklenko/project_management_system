from django.shortcuts import render

from .models import Task
from .forms import TaskForm


def index(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/index.html', {'tasks': tasks})


def task_view(request, id):
    task = Task.objects.get(id=id)
    return render(request, 'tasks/single_task.html', {'task': task})


def new_task(request):
    return render(request, 'tasks/new_task.html', {'form': TaskForm})
