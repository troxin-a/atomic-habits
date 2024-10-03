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
            SelectOneField(("related_habit", "reward", "nice")),
            MaximumNumberLimit("duration", 120),
            MaximumNumberLimit("periodicity", 7),
        )

    def get_validators(self):
        validators = super().get_validators()
        user = self.context.get("request").user
        queryset = Habit.objects.filter(user=user)

        validators.append(
            RelateByConditions("related_habit", queryset, {"nice": True}),
        )
        return validators


class HabitUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор привычки."""

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)
        validators = (
            SelectOneField(("related_habit", "reward", "nice")),
            MaximumNumberLimit("duration", 120),
            MaximumNumberLimit("periodicity", 7),
        )

    def get_validators(self):
        validators = super().get_validators()
        user = self.context.get("request").user
        queryset = Habit.objects.filter(user=user)

        validators.append(
            RelateByConditions("related_habit", queryset, {"nice": True}),
        )
        return validators

    def run_validation(self, data):
        """
        Если метод - PATCH, достает экземпляр и подмешивает нехватающие данные
        в data для полной валидации на уровне объекта
        """
        if self.context.get("request").stream.method == "PATCH":
            fields = self.get_fields().keys()

            new_data = {}
            for field in fields:
                # Вот эта страшная конструкция на самом деле сначала пытается получить значение
                # поля у объекта с окончанием _id (валидатор не принимает объекты, а только их id).
                # В конце функции, если нет такого поля с окончанием _id, получает без id
                new_data[field] = getattr(
                    self.instance,
                    (field + "_id"),
                    getattr(
                        self.instance,
                        field,
                    ),
                )
            new_data.update(data)
            data = new_data

        return super().run_validation(data)
