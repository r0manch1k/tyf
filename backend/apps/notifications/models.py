from django.db import models
from apps.profiles.models import Profile


class Notification(models.Model):
    recipient = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="notifications"
    )
    kind = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.text}"
