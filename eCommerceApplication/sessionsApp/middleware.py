from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from .models import UserSession


class UserSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get session token from request headers
        session_key = request.headers.get('Session-Token')
        
        if session_key:
            try:
                # Validate the session token
                user_session = UserSession.objects.get(session_key=session_key)
                request.user = user_session.user
            except UserSession.DoesNotExist:
                return JsonResponse({'error': 'Invalid session token'}, status=401)
        else:
            return JsonResponse({'error': 'Session token missing'}, status=401)

