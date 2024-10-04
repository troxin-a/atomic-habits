from django.db.models import ProtectedError
from rest_framework import generics, response, status
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer, HabitUpdateSerializer
from habits.services import create_task, get_task_name, update_task, delete_task


class HabitListCreateAPIView(generics.ListCreateAPIView):
    """
    Привычки.

    Создание привычек, список привычек.
    Пользователь видит только свои привычки.
    """

    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        create_task(serializer.instance)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitPublicListAPIView(generics.ListAPIView):
    """
    Опубликованные привычки.

    Видо те привычки, которые имеют статус публикации.
    """

    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Habit.objects.filter(is_published=True)


class HabitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Просмотр, редактирование, удаление привычки.

    Пользователь может управлять только своими привычками.
    """

    serializer_class = HabitUpdateSerializer
    permission_classes = (IsAuthenticated & IsOwner,)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        super().perform_update(serializer)

        instance = self.get_object()
        # if not instance.nice:
        update_task(instance)
        # else:
        #     delete_task(get_task_name(instance))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        task_name = get_task_name(instance)
        try:
            instance.delete()
        except ProtectedError:
            habits_id = [habit.id for habit in instance.habits.all()]
            return response.Response(
                data={"message": f"На удаляемую привычку ссылаются другие: {habits_id}"},
                status=status.HTTP_418_IM_A_TEAPOT,  # Ахахах )))
            )
        else:
            delete_task(task_name)
            return response.Response(status=status.HTTP_204_NO_CONTENT)
