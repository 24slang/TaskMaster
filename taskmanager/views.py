from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TaskForm, ProjectForm, NotificationSettingsForm
from .models import Task, Project, Category, Notification
from django.contrib.auth import get_user_model
from .utils import send_notification

User = get_user_model()


@login_required
def create_task(request):
    project_id = request.GET.get('project_id')
    project = None
    if project_id:
        project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = TaskForm(request.user, request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            if project:
                task.project = project
            task.save()

            if project:
                message = f"В проекте '{project.name}' создана новая задача: '{task.title}'."
                send_notification(project.users.all(), message, 'new_task')

            return redirect('taskmanager:task_list')
    else:
        form = TaskForm(request.user)

    categories = Category.objects.filter(user=request.user)

    return render(request, 'taskmanager/create_task.html', {
        'form': form,
        'categories': categories,
        'project': project,
    })


@login_required
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name, user=request.user)

            next_url = request.GET.get('next', 'taskmanager:task_list')
            return redirect(next_url)

    return render(request, 'taskmanager/create_category.html')


@login_required
def task_list(request):
    tasks = Task.objects.filter(created_by=request.user)

    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)

    priority = request.GET.get('priority')
    if priority:
        tasks = tasks.filter(priority=priority)

    project_id = request.GET.get('project')
    if project_id:
        tasks = tasks.filter(project_id=project_id)

    category_id = request.GET.get('category')
    if category_id:
        tasks = tasks.filter(category_id=category_id)

    due_date = request.GET.get('due_date')
    if due_date:
        tasks = tasks.filter(due_date__lte=due_date)

    projects = Project.objects.filter(users=request.user)
    categories = Category.objects.filter(user=request.user)

    return render(request, 'taskmanager/task_list.html', {
        'tasks': tasks,
        'projects': projects,
        'categories': categories,
    })


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, created_by=request.user)
    return render(request, 'taskmanager/task_detail.html', {'task': task})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.project:
        can_edit = (
            request.user == task.project.created_by or
            request.user in task.project.editors.all() or
            request.user == task.assigned_to
        )
    else:
        can_edit = (request.user == task.created_by)

    if not can_edit:
        raise PermissionDenied("У вас нет прав для редактирования этой задачи.")

    if request.method == 'POST':
        form = TaskForm(request.user, request.POST, instance=task)
        if form.is_valid():
            form.save()
            print(task.project)
            if task.project:
                message = f"В проекте '{task.project.name}' изменена задача: '{task.title}'."
                print("ПРОВЕРКА")
                send_notification(task.project.users.all(), message, 'task_change')

            return redirect('taskmanager:task_detail', task_id=task.id)
    else:
        form = TaskForm(request.user, instance=task)

    return render(request, 'taskmanager/edit_task.html', {
        'form': form,
        'task': task,
    })


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, created_by=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('taskmanager:task_list')

    return render(request, 'taskmanager/confirm_delete.html', {'task': task})


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()

            project.users.add(request.user)

            return redirect('taskmanager:project_list')
    else:
        form = ProjectForm()
    return render(request, 'taskmanager/create_project.html', {'form': form})


@login_required
def project_list(request):
    projects = Project.objects.filter(users=request.user)

    paginator = Paginator(projects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'taskmanager/project_list.html', {
        'page_obj': page_obj,
    })


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user not in project.users.all() and request.user not in project.editors.all():
        raise PermissionDenied("У вас нет доступа к этому проекту.")

    return render(request, 'taskmanager/project_detail.html', {
        'project': project,
    })


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('taskmanager:project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'taskmanager/edit_project.html', {
        'form': form,
        'project': project,
    })


@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('taskmanager:project_list')
    return render(request, 'taskmanager/delete_project.html', {
        'project': project,
    })


@login_required
def add_users_to_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.created_by:
        messages.error(request, "Только создатель проекта может добавлять участников.")
        return redirect('taskmanager:project_detail', project_id=project.id)

    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            project.users.add(user)
            messages.success(request, f"Пользователь {user.username} добавлен в проект.")
        except User.DoesNotExist:
            messages.error(request, f"Пользователь с именем '{username}' не найден.")

    return render(request, 'taskmanager/add_users_to_project.html', {
        'project': project,
    })


@login_required
def assign_editors(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.created_by:
        messages.error(request, "Только создатель проекта может назначать редакторов.")
        return redirect('taskmanager:project_detail', project_id=project.id)

    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            project.editors.add(user)
            messages.success(request, f"Пользователь {user.username} теперь может редактировать задачи в проекте.")
        except User.DoesNotExist:
            messages.error(request, "Пользователь с таким именем не найден.")

    return render(request, 'taskmanager/assign_editors.html', {
        'project': project,
    })


@login_required
def notification_settings(request):
    if request.method == 'POST':
        form = NotificationSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Настройки уведомлений успешно обновлены.')
            return redirect('accounts:profile')
    else:
        form = NotificationSettingsForm(instance=request.user)

    return render(request, 'taskmanager/notification_settings.html', {'form': form})


@login_required
def notifications(request):
    notifications = Notification.objects.filter(users=request.user).exclude(read_by=request.user).order_by('-created_at')

    for notification in notifications:
        notification.read_by.add(request.user)

    return render(request, 'taskmanager/notifications.html', {'notifications': notifications})
