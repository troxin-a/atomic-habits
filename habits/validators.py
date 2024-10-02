from rest_framework.serializers import ValidationError


class SelectOneField:
    """Обязывает указать одно и только одно из перечисленных полей."""

    def __init__(self, fields):
        self.fields = fields[:]
        self.str_fields = " или ".join(fields)

    def __call__(self, data):

        filled_fields = []
        for key, value in data.items():
            # Пропускает поля, которые не указаны при инициализации класса
            if key not in self.fields:
                continue

            filled_fields.append(1 if value else 0)

        if sum(filled_fields) > 1:
            raise ValidationError(f"Можно указать только одно поле: {self.str_fields}")

        if sum(filled_fields) < 1:
            raise ValidationError(f"Обязательно нужно указать одно из полей: {self.str_fields}")


class MaximumNumberLimit:
    """Ограничивает введенное число в диапазон от 1 до limit."""

    def __init__(self, field, limit):
        self.field = field
        self.limit = limit

    def __call__(self, value):
        if not (0 < value.get(self.field) <= self.limit):
            raise ValidationError(f"{self.field}: Введите число от 1 до {self.limit}")


class RelateByConditions:
    """
    Подключение объекта по foreign_key по предоставленном условиям {"Поле": "Значение", ...}).
    """

    def __init__(self, field, queryset, conditions):
        self.field = field
        self.queryset = queryset
        self.conditions = conditions

    def __call__(self, data):
        foreign_obj = data.get(self.field)

        for key, cond_value in self.conditions.items():
            foreign_obj_value = getattr(foreign_obj, key, 'default')
            if foreign_obj_value != cond_value:
                raise ValidationError(f"{self.field}: Поле '{key}' у объекта {foreign_obj.id} должно быть '{cond_value}'")
