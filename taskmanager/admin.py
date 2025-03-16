from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'category', 'created_by')
    list_filter = ('project', 'category')

    def save_model(self, request, obj, form, change):
        # Проверка перед сохранением в админке
        if obj.project and obj.category:
            raise ValidationError("Задача не может быть привязана к проекту и категории одновременно.")
        super().save_model(request, obj, form, change)
