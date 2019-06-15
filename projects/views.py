from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages

from .models import Project
from tasks.models import Task
from .forms import ProjectForm, TaskForm


def index(request):
    projects = Project.objects.all().order_by('-id')
    return render(request, 'projects/index.html', {'projects': projects})


def project_view(request, id):
    project = get_object_or_404(Project, id=id)
    tasks = Task.objects.filter(project=id)

    return render(request, 'projects/single_project.html', {'project': project, 'tasks': tasks})


def new_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            messages.add_message(request, messages.INFO,
                                 'Project "{}" was successfully created'.format(project.title))
            return redirect('/projects')
    else:
        form = ProjectForm()

    return render(request, 'projects/new_project.html', {'form': form})


def edit_project(request, id):
    project = get_object_or_404(Project, id=id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,
                                 'Project "{}" was successfully updated'.format(project.title))
            return redirect(reverse('project', args=[project.id]))
    else:
        form = ProjectForm(instance=project)

    context = {
        'project': project,
        'form': form
    }
    return render(request, 'projects/edit_project.html', context)


def new_task(request, project_id):

    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, project_id=project_id)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.project = project
            task.save()
            messages.add_message(request, messages.INFO,
                                 'Task "{}" was successfully created in project "{}"'.format(task.title, project.title))
            return redirect(reverse('projects:project', args=[project_id]))
        pass
    else:
        form = TaskForm(project_id=project_id)

    return render(request, 'projects/new_task.html', {'form': form})
