from django.shortcuts import render, redirect
from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse

from .models import Task
from .forms import TaskForm
from projects.models import Project


def index(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/index.html', {'tasks': tasks})


def task_view(request, id):
    task = Task.objects.get(id=id)
    return render(request, 'tasks/single_task.html', {'task': task})


def new_task(request):
    project = Project.objects.get(id=request.GET['project_id'])
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.project = project
            messages.add_message(request, messages.INFO,
                                 'Task "{}" was successfully created in project "{}"'.format(task.title, project.title))
            task.save()
            return redirect(reverse('project', args=[project.id]))
        pass
    else:
        form = TaskForm()
        form.fields['assigned_to'].queryset = User.objects.filter(
            projects__id=project.id)

    return render(request, 'tasks/new_task.html', {'form': form})
