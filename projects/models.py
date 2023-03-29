from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """
    Model to store user-created projects
    Links to creator (User instance)
    """
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects'
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
    Links to creator (User instance) and project (Project instance) 
    """
    summary = models.CharField(max_length=100)
    body = models.TextField()
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
