from .models import Notification


def unread_notifications_count(request):
    if request.user.is_authenticated:
        return {'unread_notifications_count': Notification.objects.filter(user=request.user).count()}
    return {}