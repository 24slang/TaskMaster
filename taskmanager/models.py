from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'Высокий'),
        ('medium', 'Средний'),
        ('low', 'Низкий'),
    ]

    STATUS_CHOICES = [
        ('todo', 'К выполнению'),
        ('in_progress', 'В процессе'),
        ('done', 'Выполнено'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, blank=True)  # Необязательное поле
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)  # Необязательное поле
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_status_color(self):
        if self.status == 'todo':
            return 'secondary'
        elif self.status == 'in_progress':
            return 'warning'
        elif self.status == 'done':
            return 'success'
        return 'primary'


class Project(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    users = models.ManyToManyField(User, related_name='projects')
    editors = models.ManyToManyField(User, related_name='editable_projects', blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name


class Notification(models.Model):
    users = models.ManyToManyField(User, related_name='notifications')
    read_by = models.ManyToManyField(User, related_name='read_notifications', blank=True)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Уведомление для {self.user.username}: {self.message}"

    def is_read_by_user(self, user):
        """Проверяет, прочитал ли пользователь уведомление."""
        return self.read_by.filter(id=user.id).exists()
