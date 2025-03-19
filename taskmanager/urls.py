from django.urls import path
from .views import (
    task_list,
    create_task,
    create_category,
    task_detail,
    edit_task,
    delete_task,
    create_project,
    project_list,
    project_detail,
    edit_project,
    delete_project,
    add_users_to_project,
    assign_editors,
    notification_settings,
    notifications,
)


app_name = "taskmanager"

urlpatterns = [
    path('task-list', task_list, name='task_list'),

    path('create-task', create_task, name='create_task'),
    path('create-category', create_category, name='create_category'),

    path('project-list/', project_list, name='project_list'),
    path('create-project/', create_project, name='create_project'),

    path('task/<int:task_id>/', task_detail, name='task_detail'),
    path('task/<int:task_id>/edit/', edit_task, name='edit_task'),
    path('task/<int:task_id>/delete/', delete_task, name='delete_task'),

    path('project/<int:project_id>/', project_detail, name='project_detail'),
    path('project/<int:project_id>/edit/', edit_project, name='edit_project'),
    path('project/<int:project_id>/delete/', delete_project, name='delete_project'),

    path('project/<int:project_id>/add-users/', add_users_to_project, name='add_users_to_project'),
    path('project/<int:project_id>/assign-editors/', assign_editors, name='assign_editors'),

    path('notifications/', notifications, name='notifications'),
    path('notification-settings/', notification_settings, name='notification_settings'),
]
