from django.contrib.sessions.models import Session
from django.utils import timezone

class LimitSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            print('holaaaaaaaaaaaaaaaaaaaa')
            max_sessions = 3  # Cambia esto al número deseado de sesiones permitidas
            active_sessions = Session.objects.filter(
                expire_date__gte=timezone.now(),
                session_key__in=request.user.session_set.values_list('session_key', flat=True)
            )
            if active_sessions.count() > max_sessions:
                # Cierra las sesiones adicionales
                print("Se ha superado el límite de sesiones.")
                for session in active_sessions[max_sessions:]:
                    session.expire_date = timezone.now()
                    session.save()
        response = self.get_response(request)
        return response
