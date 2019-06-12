from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.models import User

from .models import Task


class TaskForm(ModelForm):
    assigned_to = ModelChoiceField(
        queryset=User.objects.filter(projects__id=1)
    )

    class Meta:
        model = Task
        fields = ['title', 'body', 'assigned_to', 'estimated_time', ]
