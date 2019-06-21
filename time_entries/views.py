from django.shortcuts import render
from django.core.paginator import Paginator

from .models import TimeEntry


def index(request):
    time_entries = TimeEntry.objects.order_by('-id')

    paginator = Paginator(time_entries, 20)
    page = request.GET.get('page')
    time_entries = paginator.get_page(page)
    full_path = request.get_full_path()

    context = {
        'time_entries': time_entries,
        'full_path': full_path
    }

    return render(request, 'time_entries/index.html', context)
