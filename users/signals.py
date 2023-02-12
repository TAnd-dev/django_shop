"""
Import required libraries for signals
"""
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser, UserProfile


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    """
    This function is a post_save signal receiver for the `CustomUser` model.
    It creates a `UserProfile` object for each newly created `CustomUser` instance.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    """
    This function is a post_save signal receiver for the `CustomUser` model.
    It saves the related `UserProfile` object when a `CustomUser` instance is saved.
    """
    instance.profile.save()
