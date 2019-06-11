from django.contrib import admin

from .models import Project, Status

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass