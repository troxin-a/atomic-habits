from rest_framework import serializers

from habits.models import Habit
from habits.validators import SelectOneField, MaximumNumberLimit, RelateByConditions


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор привычки."""

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)
        validators = (
            SelectOneField(("related_habit", "reward")),
            MaximumNumberLimit("duration", 120),
            RelateByConditions("related_habit", model.objects.all(), {"nice": True, "place": "Привет"}),
        )
