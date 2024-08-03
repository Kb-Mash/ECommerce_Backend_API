from django.db import models
from django.conf import settings


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

    def __str__(self):
        """
        Returns:
            str: A string indicating the user and session key.
        """
        return f'Session for {self.user.username} with key {self.session_key}'
