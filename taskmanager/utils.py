from .models import Notification


def create_notification(user, message):
    """
    Создает уведомление для пользователя.
    """
    Notification.objects.create(users=user, message=message)


def send_notification(users, message, notification_type):
    """
    Отправляет уведомления пользователям, если они включили соответствующие настройки.
    """
    for user in users:
        if notification_type == 'new_task' and user.notify_new_tasks:
            print(f"Отправка уведомления о новой задаче пользователю {user.username}")
            notification = Notification.objects.create(message=message)
            notification.users.add(user)
        elif notification_type == 'task_change' and user.notify_task_changes:
            print(f"Отправка уведомления об изменении задачи пользователю {user.username}")
            notification = Notification.objects.create(message=message)
            notification.users.add(user)
        elif notification_type == 'deadline' and user.notify_deadlines:
            print(f"Отправка уведомления о дедлайне пользователю {user.username}")
            notification = Notification.objects.create(message=message)
            notification.users.add(user)

