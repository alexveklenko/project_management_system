from django.forms import ModelForm, ModelMultipleChoiceField
from django.contrib.auth.models import User

from django_select2.forms import Select2MultipleWidget

from .models import Project


class ProjectForm(ModelForm):
    members = ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=Select2MultipleWidget
    )

    class Meta:
        model = Project
        fields = ['title', 'body', 'status', 'members', ]
