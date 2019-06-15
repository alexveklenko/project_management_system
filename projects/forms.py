from django.forms import ModelForm, ModelMultipleChoiceField, ModelChoiceField
from django.contrib.auth.models import User

from django_select2.forms import Select2MultipleWidget

from .models import Project
from tasks.models import Task


class ProjectForm(ModelForm):
    members = ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=Select2MultipleWidget
    )

    class Meta:
        model = Project
        fields = ['title', 'body', 'status', 'members', ]


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id')
        super().__init__(*args, **kwargs)

        self.fields['assigned_to'].queryset = User.objects.filter(
            projects__id=project_id)

    class Meta:
        model = Task
        fields = ['title', 'body', 'assigned_to',
                  'estimated_time', 'status', 'priority', ]
