from datetime import datetime
import pytz
from django.utils import timezone
from .models import UserProfile


def theme_context(request):
    """Context processor для определения темы по времени пользователя"""
    context = {
        'is_dark_theme': False,
        'current_time': timezone.now(),
        'user_timezone': 'UTC'
    }
    
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            user_timezone = profile.timezone
            user_tz = pytz.timezone(user_timezone)
            
            # Получаем текущее время в часовом поясе пользователя
            current_time = timezone.now().astimezone(user_tz)
            current_hour = current_time.hour
            
            # Определяем тему: темная с 18:00 до 6:00
            is_dark_theme = current_hour >= 18 or current_hour < 6
            
            context.update({
                'is_dark_theme': is_dark_theme,
                'current_time': current_time,
                'user_timezone': user_timezone,
                'current_hour': current_hour
            })
            
        except (UserProfile.DoesNotExist, pytz.UnknownTimeZoneError):
            # Если профиль не найден или часовой пояс некорректен, используем UTC
            current_time = timezone.now()
            current_hour = current_time.hour
            is_dark_theme = current_hour >= 18 or current_hour < 6
            
            context.update({
                'is_dark_theme': is_dark_theme,
                'current_time': current_time,
                'current_hour': current_hour
            })
    
    return context 