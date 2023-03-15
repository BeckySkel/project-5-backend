from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from allauth.account.signals import email_confirmed


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    profile = email_address.user.profile
    print(profile)
    profile.email_verified = True

    profile.save()


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
