from django.db import models


class Status(models.Model):
    title = models.CharField(max_length=255)

    class Meta():
        verbose_name_plural = 'Statuses'

    def __str__(self):
        return self.title


class Priority(models.Model):
    title = models.CharField(max_length=255)

    class Meta():
        verbose_name_plural = 'Priority'

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE
    )
    added = models.DateTimeField(auto_now_add=True)
    estimated_time = models.PositiveIntegerField(default=0)
    spent_time = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(
        'auth.User',
        related_name='author_of',
        on_delete=models.CASCADE
    )
    assigned_to = models.ForeignKey(
        'auth.User',
        related_name='responsive_for',
        on_delete=models.CASCADE
    )
    status = models.ForeignKey(
        'Status',
        on_delete=models.CASCADE
    )
    priority = models.ForeignKey(
        'Priority',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
