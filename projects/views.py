from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse

from .models import Project
from tasks.models import Task
from .forms import ProjectForm


def index(request):
    projects = Project.objects.all()
    return render(request, 'projects/index.html', {'projects': projects})


def project_view(request, id):
    project = get_object_or_404(Project, id=id)
    tasks = Task.objects.all().filter(project=id)
    return render(request, 'projects/single_project.html', {'project': project, 'tasks': tasks})


def new_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
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
            return redirect(reverse('project', args=[project.id]))
    else:
        form = ProjectForm(instance=project)

    context = {
        'project': project,
        'form': form
    }
    return render(request, 'projects/edit_project.html', context)
