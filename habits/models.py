from django.db import models

NULLABLE = {"blank": True, "null": True}


class Habit(models.Model):
    user = models.ForeignKey(
        to="users.User",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="habits",
    )
    place = models.CharField(
        verbose_name="Место выполнения",
        max_length=150,
    )
    time = models.DateTimeField(
        verbose_name="Дата и время выполнения",
    )
    doing = models.CharField(
        verbose_name="Действие",
        max_length=150,
    )
    nice = models.BooleanField(
        verbose_name="Приятная привычка",
        default=False,
    )
    related_habit = models.ForeignKey(
        to="self",
        verbose_name="Связанная привычка",
        on_delete=models.PROTECT,
        related_name="habits",
        **NULLABLE,
    )
    periodicity = models.SmallIntegerField(
        verbose_name="Периодичность (дней)",
        default=1,
    )
    reward = models.CharField(
        verbose_name="Вознаграждение",
        max_length=150,
        **NULLABLE,
    )
    duration = models.SmallIntegerField(
        verbose_name="Продолжительность выполнения (сек)",
        default=1,
    )
    is_published = models.BooleanField(
        verbose_name="Признак публикации",
        default=False,
    )

    def __str__(self) -> str:
        return self.doing

    class Meta:
        verbose_name = ("привычка",)
        verbose_name_plural = ("привычки",)
        ordering = ("-id",)
