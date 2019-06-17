from django.db import models


class TimeEntry(models.Model):
    comment = models.TextField(
        blank=True
    )
    spent_time = models.PositiveIntegerField()
    added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )
    task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'Time entries'

    def __str__(self):
        return self.comment[:30]
