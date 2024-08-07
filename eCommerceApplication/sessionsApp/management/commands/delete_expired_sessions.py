from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from sessionsApp.models import UserSession

class Command(BaseCommand):
    help = 'Delete expired sessions'

    def handle(self, *args, **kwargs):
        expired_sessions = UserSession.objects.filter(expires_at__lt=timezone.now())
        count, _ = expired_sessions.delete()
        self.stdout.write(f'Deleted {count} expired sessions.')

