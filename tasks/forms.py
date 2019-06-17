from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.models import User

from django_select2.forms import Select2Widget

from .models import Task
from projects.models import Project
from time_entries.models import TimeEntry


class TaskForm(ModelForm):
    project = ModelChoiceField(
        queryset=Project.objects.all(),
        widget=Select2Widget
    )

    class Meta:
        model = Task
        fields = ['title', 'body', 'project', 'assigned_to',
                  'estimated_time', 'status', 'priority', ]


class LogTimeForm(ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['comment', 'spent_time', ]
