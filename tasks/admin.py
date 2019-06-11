from django.contrib import admin

from .models import Task, Status, Priority


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    pass
