from django.db import models
from django.conf import settings
# Session Token Expiry
from django.utils import timezone
from datetime import timedelta


class UserSession(models.Model):
    """
    Represents an active session for any user in the system.

    Attributes:
        user (ForeignKey): The user associated with this session.
        session_key (CharField): The unique session key.
        created_at (DateTimeField): The timestamp when the session was created.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=lambda: timezone.now() + timedelta(hours=1))

    def __str__(self):
        """
        Returns:
            str: A string indicating the user and session key.
        """
        return f'Session for {self.user.username} with key {self.session_key}'

    def is_expired(self):
        return timezone.now() > self.expires_at
