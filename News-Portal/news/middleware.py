import pytz
from django.utils import timezone
from django.contrib.auth.models import User
from .models import UserProfile


class TimezoneMiddleware:
    """Middleware для автоматической установки часового пояса пользователя"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Получаем часовой пояс пользователя
        if request.user.is_authenticated:
            try:
                user_timezone = request.user.profile.timezone
                timezone.activate(pytz.timezone(user_timezone))
            except (UserProfile.DoesNotExist, pytz.UnknownTimeZoneError):
                # Если профиль не найден или часовой пояс некорректен, используем UTC
                timezone.activate(pytz.UTC)
        else:
            # Для неаутентифицированных пользователей используем UTC
            timezone.activate(pytz.UTC)
        
        response = self.get_response(request)
        timezone.deactivate()
        return response 