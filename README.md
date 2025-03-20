# TaskMaster

**TaskMaster** — это веб-приложение для управления задачами и проектами. Оно позволяет пользователям создавать, редактировать, удалять и отслеживать задачи, а также управлять проектами и получать уведомления о важных событиях.

---

## Основные функции

### Регистрация и аутентификация пользователей
- Регистрация новых пользователей с использованием электронной почты и пароля.
- Аутентификация пользователей.
- Восстановление пароля через электронную почту.

### Управление задачами
- Создание задач с указанием заголовка, описания, сроков выполнения, приоритета и категории.
- Просмотр, редактирование и удаление задач.
- Фильтрация и поиск задач по статусу, приоритету, срокам выполнения и другим параметрам.

### Управление проектами
- Создание проектов и привязка задач к ним.
- Просмотр списка задач, связанных с конкретным проектом.
- Назначение ответственных лиц для выполнения задач в рамках проекта.

### Уведомления и оповещения
- Автоматическая отправка уведомлений о новых задачах, изменениях и напоминаниях о сроках выполнения.
- Настройка предпочтений уведомлений для каждого пользователя.

### Интерфейс пользователя
- Интуитивно понятный и адаптивный интерфейс, разработанный с использованием **Bootstrap**.
- Поддержка различных устройств: компьютеры, планшеты, мобильные телефоны.

### Безопасность
- Защита данных пользователей с использованием шифрования.
- Разграничение прав доступа в зависимости от роли пользователя (администратор, обычный пользователь).

---

## Установка и запуск

### Требования
- Python 3.8 или выше
- Django 4.0 или выше
- База данных (например, PostgreSQL, SQLite)
- Установленные зависимости из `requirements.txt`

### Шаги для установки
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш-username/TaskMaster.git
   cd TaskMaster
