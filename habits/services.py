import json
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, IntervalSchedule


def get_message_text(habit):
    """Формирует текст для отправки сообщения."""

    time = timezone.localtime(habit.time).strftime("%d.%m.%Y %H:%M")
    text = f"Уже {time}!\nПора {habit.doing.lower()} {habit.duration} сек.\nМесто: {habit.place.lower()}\n"
    if habit.reward:
        text += f"Награда: {habit.reward.lower()}."
    if habit.related_habit:
        text += f"Далее можно будет: {habit.related_habit.doing.lower()} {habit.related_habit.duration} сек."
    if habit.nice:
        text += "Это приятная привычка."
    return text


def get_task_name(habit):
    """Формирует уникальное название задачи"""
    return f"task_{habit.id}_user{habit.user_id}"


def get_interval(periodicity):
    """Возвращает новый либо существующий интервал."""

    schedule, created = IntervalSchedule.objects.get_or_create(
        every=periodicity,
        period=IntervalSchedule.DAYS,
    )
    return schedule or created


def create_task(habit):
    """Создает периодическую задачу."""

    task = PeriodicTask.objects.create(
        name=get_task_name(habit),
        task="habits.tasks.send_message",
        interval=get_interval(habit.periodicity),
        start_time=habit.time,
        kwargs=json.dumps(
            {
                "chat_id": habit.user.tg_chat_id,
                "text": get_message_text(habit),
            }
        ),
    )
    if habit.nice:
        task.enabled = False
        task.save()


def update_task(habit):
    """
    Обновляет периодическую задачу.
    Если она не найдена, создает новую.
    """

    task = PeriodicTask.objects.filter(name=get_task_name(habit)).first()
    if not task:
        create_task(habit)
        return

    task.interval = get_interval(habit.periodicity)
    task.kwargs = json.dumps(
        {
            "chat_id": habit.user.tg_chat_id,
            "text": get_message_text(habit),
        }
    )
    task.start_time = habit.time
    if habit.nice:
        task.enabled = False
    else:
        task.enabled = True
    task.save()


def delete_task(task_name):
    """Удаляет периодическую задачу по ее имени."""

    PeriodicTask.objects.filter(name=task_name).delete()
