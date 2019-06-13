from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.models import User

from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'body', 'assigned_to',
                  'estimated_time', 'status', 'priority', ]
