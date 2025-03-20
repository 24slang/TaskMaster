from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    notify_new_tasks = models.BooleanField(default=True, verbose_name="Уведомления о новых задачах")
    notify_task_changes = models.BooleanField(default=True, verbose_name="Уведомления об изменениях задач")
    notify_deadlines = models.BooleanField(default=True, verbose_name="Уведомления о дедлайнах")
