from .models import Announcement, Event
from django.utils import timezone


def global_context(request):
    if not request.user.is_authenticated:
        return {}
    announcements = Announcement.objects.filter(is_active=True)[:5]
    upcoming_events = Event.objects.filter(event_date__gte=timezone.now().date()).order_by('event_date')[:3]
    return {
        'global_announcements': announcements,
        'global_events': upcoming_events,
        'user_role': request.user.role,
    }
