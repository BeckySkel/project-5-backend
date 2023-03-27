import uuid
from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """
    Model to store user-created projects
    Links to creator (user instance)
    """
    title = models.CharField(max_length=100)
    url_id = models.UUIDField(
         default=uuid.uuid4,
         editable=False)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects'
        )
    contributors = models.ManyToManyField(
        User,
        related_name='contrib_projects',
        blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Task(models.Model):
    """
    Model to store tasks for projects
    Links to creator (user instance)
    """
    summary = models.CharField(max_length=100)
    body = models.TextField()
    due_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks'
        )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
        )

    class Meta:
        ordering = ['-updated_on']

    def __str__(self):
        return f'{self.summary} by {self.creator}'
