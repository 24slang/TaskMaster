from django import forms
from django.contrib.auth import get_user_model

from .models import Task, Project, Category


User = get_user_model()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status', 'project', 'category', 'assigned_to']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(editors=user)
        self.fields['category'].queryset = Category.objects.filter(user=user)


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name']


class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['notify_new_tasks', 'notify_task_changes', 'notify_deadlines']
        labels = {
            'notify_new_tasks': 'Уведомления о новых задачах',
            'notify_task_changes': 'Уведомления об изменениях задач',
            'notify_deadlines': 'Уведомления о дедлайнах',
        }