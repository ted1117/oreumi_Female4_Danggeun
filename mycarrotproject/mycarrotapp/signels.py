from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from mycarrotapp.models import UserInfo

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
