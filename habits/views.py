from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание привычки."""

    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class HabitRetrieveAPIView(generics.RetrieveAPIView):
#     """
#     Регистрация.
#     Только авторизованный пользователь может зарегистрироваться
#     """

#     serializer_class = RegisterSerializer
#     permission_classes = (~IsAuthenticated,)