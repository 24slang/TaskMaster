from celery import shared_task
from django.utils import timezone
from .models import Task, Notification

@shared_task
def send_deadline_notifications():
    # Находим задачи, у которых дедлайн через 24 часа
    deadline = timezone.now() + timezone.timedelta(hours=24)
    tasks = Task.objects.filter(due_date__lte=deadline, due_date__gt=timezone.now())

    for task in tasks:
        if task.assigned_to and task.assigned_to.notify_deadlines:
            message = f"Дедлайн задачи '{task.title}' наступит {task.due_date}."
            Notification.objects.create(user=task.assigned_to, message=message)