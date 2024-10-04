from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from users.models import User
from users.serializers import (
    UserSerializer,
    RegisterSerializer,
    PasswordUpdateSerializer,
)


class UserCreateAPIView(generics.CreateAPIView):
    """
    Регистрация.

    Только неавторизованный пользователь может зарегистрироваться.
    """

    serializer_class = RegisterSerializer
    permission_classes = (~IsAuthenticated,)

    @swagger_auto_schema(responses={200: RegisterSerializer()})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Профиля пользователя.

    Только авторизованный пользователь видит и редактирует свой профиль.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserPasswordUpdateAPIView(generics.UpdateAPIView):
    """
    Смена пароля.

    Необходимо ввести новый и старый пароль.
    """

    queryset = User.objects.all()
    serializer_class = PasswordUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Неверный пароль"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"message": "Пароль успешно изменен"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
