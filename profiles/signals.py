from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# code to connect Profile database to User from tutorial at
# https://www.youtube.com/watch?v=Kc1Q_ayAeQk
@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    """
    Signal creates new profile after user registers, checks if creating or
    updating profile first.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
