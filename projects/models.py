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
        related_name='recipe_posts'
        )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    removed = models.BooleanField(default=False)
    private = models.BooleanField(default=False)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
