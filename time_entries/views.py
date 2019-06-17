from django.shortcuts import render

from .models import TimeEntry


def index(request):
    time_entries = TimeEntry.objects.all()
    context = {
        'time_entries': time_entries
    }
    return render(request, 'time_entries/index.html', context)
