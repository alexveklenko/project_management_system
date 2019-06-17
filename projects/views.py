from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Project, Status
from tasks.models import Task
from .forms import ProjectForm, TaskForm


def index(request):
    print('*'*100)
    print(request.GET)

    projects = Project.objects.all().order_by('-id')
    users = User.objects.all()
    statuses = Status.objects.all()

    f_search = request.GET.get('search', '')

    if f_search:
        projects = projects.filter(title__icontains=f_search)

    context = {
        'projects': projects,
        'users': users,
        'statuses': statuses,
        'f_search': f_search
    }

    return render(request, 'projects/index.html', context)


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
