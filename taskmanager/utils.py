from .models import Notification


def create_notification(user, message):
    """
    Создает уведомление для пользователя.
    """
    Notification.objects.create(users=user, message=message)
