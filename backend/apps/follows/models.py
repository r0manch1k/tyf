from django.db import models
from apps.profiles.models import Profile


class Follow(models.Model):
    follower = models.ForeignKey(
        Profile, related_name="following", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        Profile, related_name="followers", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} followed {self.following} at {self.created_at}"
