from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from .models import Profile


User = get_user_model()


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance, email=instance.email, date_joined=instance.date_joined
        )


post_save.connect(create_profile, sender=User, dispatch_uid="create_profile")
