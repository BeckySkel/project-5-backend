from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    """
    Model to store extra information about the user.
    Created/updated/deleted automatically when a new user is
    added/updated/deleted via signals.py
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
        )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    created_on = models.DateField(auto_now_add=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ["-created_on"]
