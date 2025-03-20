from .models import Notification


def unread_notifications_count(request):
    if request.user.is_authenticated:
        unread_notifications_count = Notification.objects.filter(users=request.user).exclude(read_by=request.user).count()
        return {'unread_notifications_count': unread_notifications_count}
    return {}