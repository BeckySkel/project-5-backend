import uuid
from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """
    Model to store user-created projects
    """
    title = models.CharField(max_length=100, unique=True)
    url_id = models.UUIDField(
         default=uuid.uuid4,
         editable=False)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects'
        )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    removed = models.BooleanField(default=False)
    private = models.BooleanField(default=False)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Task(models.Model):
    """
    Model to store tasks for projects
    """
    summary = models.CharField(max_length=100, unique=True)
    body = models.TextField()
    due_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
        )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
        )

    def __str__(self):
        return f'{self.summary} by {self.creator}'
