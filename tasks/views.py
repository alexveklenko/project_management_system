from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.core.mail import send_mail

from .models import Task, Status, Priority
from .forms import TaskForm, LogTimeForm
from projects.forms import TaskForm as ProjectTaskForm
from projects.models import Project
from time_entries.models import TimeEntry


def index(request):
    # send_mail(
    #     'Subject here',
    #     'Here is the message.',
    #     'from@example.com',
    #     ['alexi.veklenko@gmail.com'],
    #     fail_silently=False
    # )

    tasks = Task.objects.order_by('-id')
    projects = Project.objects.all()
    statuses = Status.objects.all()
    priorities = Priority.objects.all()
    users = User.objects.all()

    f_search = request.GET.get('search', '')
    f_project = request.GET.get('project')
    f_status = request.GET.get('status')
    f_priority = request.GET.get('priority')
    f_author = request.GET.get('author')
    f_member = request.GET.get('member')

    selected_project = None
    selected_status = None
    selected_priority = None
    selected_author = None
    selected_member = None

    if f_search:
        tasks = tasks.filter(title__icontains=f_search)

    if f_project and f_project != 'all':
        selected_project = int(f_project)
        tasks = tasks.filter(project__id=selected_project)

    if f_status and f_status != 'all':
        selected_status = int(f_status)
        tasks = tasks.filter(status=selected_status)

    if f_priority and f_priority != 'all':
        selected_priority = int(f_priority)
        tasks = tasks.filter(priority=selected_priority)

    if f_author and f_author != 'all':
        selected_author = int(f_author)
        projects = projects.filter(author=f_author)

    if f_member and f_member != 'all':
        selected_member = int(f_member)
        projects = projects.filter(members=f_member)

    paginator = Paginator(tasks, 20)
    page = request.GET.get('page')
    tasks = paginator.get_page(page)
    full_path = request.get_full_path()

    context = {
        'tasks': tasks,
        'projects': projects,
        'statuses': statuses,
        'priorities': priorities,
        'users': users,
        'f_search': f_search,
        'selected_project': selected_project,
        'selected_status': selected_status,
        'selected_priority': selected_priority,
        'selected_author': selected_author,
        'selected_member': selected_member,
        'full_path': full_path,
    }

    return render(request, 'tasks/index.html', context)


def task_view(request, id):
    task = Task.objects.get(id=id)
    time_entries = TimeEntry.objects.filter(task=task.id)
    user_can_edit = request.user.is_superuser or request.user == task.assigned_to
    user_can_log_time = request.user == task.assigned_to
    context = {
        'task': task,
        'time_entries': time_entries,
        'user_can_edit': user_can_edit,
        'user_can_log_time': user_can_log_time,
    }
    return render(request, 'tasks/single_task.html', context)


def new_task(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Access denied')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            messages.add_message(request, messages.INFO,
                                 'Task "{}" was successfully created in project "{}"'.format(task.title, task.project))
            return redirect(reverse('tasks:tasks'))
    else:
        form = TaskForm()

    context = {
        'form': form
    }

    return render(request, 'tasks/new_task.html', context)


def edit_task(request, id):
    task = Task.objects.get(id=id)
    if not request.user.is_superuser and request.user != task.assigned_to:
        return HttpResponseForbidden('Access denied')

    if request.method == 'POST':
        form = ProjectTaskForm(
            request.POST, project_id=task.project.id, instance=task)
        project = Project.objects.get(id=task.project.id)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.project = project
            task.save()
            messages.add_message(
                request,
                messages.INFO,
                'Task "{}" was successfully updated in project "{}"'.format(
                    task.title, task.project)
            )
            return redirect(reverse('tasks:tasks'))

    else:
        form = ProjectTaskForm(project_id=task.project.id, instance=task)

    context = {
        'task': task,
        'form': form
    }
    return render(request, 'tasks/edit_task.html', context)


def log_time(request, id):
    task = Task.objects.get(id=id)
    project = Project.objects.get(id=task.project.id)

    if request.user != task.assigned_to:
        return HttpResponseForbidden('Access denied')

    if request.method == 'POST':
        form = LogTimeForm(request.POST)
        if form.is_valid():
            time_entry = form.save(commit=False)
            time_entry.author = request.user
            time_entry.task = task

            task.spent_time += time_entry.spent_time
            project.spent_time += time_entry.spent_time

            time_entry.save()
            task.save()
            project.save()

            messages.add_message(
                request,
                messages.INFO,
                'Spent time on task "{}" has been updated'.format(task.title)
            )

            return redirect(reverse('time_entries:spent_time'))

    else:
        form = LogTimeForm()

    context = {
        'form': form
    }

    return render(request, 'tasks/log_time.html', context)


def ajax_get_members(request):
    # update members in create-tast-form when project is changed
    members = User.objects.filter(projects__id=request.GET['project_id'])
    choices = '<option value="" selected>---------</option>'

    for member in members:
        choices += '<option value="{}">{}</option>'.format(
            member.id, member.username)

    return JsonResponse({'markup': choices})
