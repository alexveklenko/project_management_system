from django.db import models


class Status(models.Model):
    title = models.CharField(max_length=225)

    class Meta:
        verbose_name_plural = 'Statuses'

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=225)
    body = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(
        Status,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        'auth.User',
        related_name='created_projects',
        on_delete=models.CASCADE,
    )
    members = models.ManyToManyField(
        'auth.User',
        related_name='projects',
        blank=True
    )
    spent_time = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def body_as_html(self):
        import markdown
        return markdown.markdown(self.body)
