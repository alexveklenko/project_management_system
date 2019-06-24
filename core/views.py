from django.shortcuts import render
from django.db.models import Q

from projects.models import Project
from tasks.models import Task
from time_entries.models import TimeEntry


def index(request):
    return render(request, 'core/index.html', {})


def global_search(request):
    context = {}
    if request.method == 'GET':
        q_search = request.GET.get('search')

        if q_search:
            context['q_search'] = q_search
            context['projects'] = Project.objects.filter(
                Q(title__icontains=q_search) | Q(body__icontains=q_search)
            )
            context['tasks'] = Task.objects.filter(
                Q(title__icontains=q_search) | Q(body__icontains=q_search)
            )
            context['time_entries'] = TimeEntry.objects.filter(
                comment__icontains=q_search
            )

    return render(request, 'core/global_search.html', context)
