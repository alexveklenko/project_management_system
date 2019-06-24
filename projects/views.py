from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from .models import Project, Status
from tasks.models import Task
from .forms import ProjectForm, TaskForm


def index(request):
    projects = Project.objects.order_by('-id')
    users = User.objects.all()
    statuses = Status.objects.all()

    f_search = request.GET.get('search', '')
    f_author = request.GET.get('author')
    f_member = request.GET.get('member')
    f_status = request.GET.get('status')
    selected_author = None
    selected_member = None
    selected_status = None

    if f_search:
        projects = projects.filter(title__icontains=f_search)

    if f_author and f_author != 'all':
        selected_author = int(f_author)
        projects = projects.filter(author=f_author)

    if f_member and f_member != 'all':
        selected_member = int(f_member)
        projects = projects.filter(members=f_member)

    if f_status and f_status != 'all':
        selected_status = int(f_status)
        projects = projects.filter(status=f_status)

    paginator = Paginator(projects, 20)
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    full_path = request.get_full_path()

    context = {
        'projects': projects,
        'users': users,
        'statuses': statuses,
        'f_search': f_search,
        'selected_author': selected_author,
        'selected_member': selected_member,
        'selected_status': selected_status,
        'full_path': full_path
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
            return redirect(reverse('projects:project', args=[project.id]))
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
