from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse

from .models import Task
from .forms import TaskForm, LogTimeForm
from projects.forms import TaskForm as ProjectTaskForm
from projects.models import Project
from time_entries.models import TimeEntry


def index(request):
    tasks = Task.objects.all().order_by('-id')
    return render(request, 'tasks/index.html', {'tasks': tasks})


def task_view(request, id):
    task = Task.objects.get(id=id)
    time_entries = TimeEntry.objects.filter(task=task.id)
    context = {
        'task': task,
        'time_entries': time_entries
    }
    return render(request, 'tasks/single_task.html', context)


def new_task(request):
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

    if request.method == 'POST':
        pass
    else:
        print('*'*100)
        print(task.project.id)
        form = ProjectTaskForm(project_id=task.project.id, instance=task)

    context = {
        'task': task,
        'form': form
    }
    return render(request, 'tasks/edit_task.html', context)


def log_time(request, id):
    if request.method == 'POST':
        form = LogTimeForm(request.POST)
        if form.is_valid():
            task = Task.objects.get(id=id)
            project = Project.objects.get(id=task.project.id)
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
    members = User.objects.filter(projects__id=request.GET['project_id'])
    choices = '<option value="" selected>---------</option>'

    for member in members:
        choices += '<option value="{}">{}</option>'.format(
            member.id, member.username)

    return JsonResponse({'markup': choices})
