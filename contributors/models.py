from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


class Contributor(models.Model):
    """
    Model to store project contributors
    All 3 fields must be unique together (no duplicates)
    """
    user = models.ForeignKey(
        User, related_name='contributing_to', on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        Project, related_name='contributors', on_delete=models.CASCADE
    )
    creator = models.ForeignKey(
        User, related_name='invitees', on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ['user', 'project', 'creator']

    def __str__(self):
        return f'{self.user} {self.project}'
