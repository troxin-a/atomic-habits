from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User


class UserTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(email="user1@test.ru", tg_chat_id="0")
        self.user1.set_password("1")

    def test_user_create(self):
        """Тест на регистрацию"""

        url = reverse("users:create")
        data = {
            "email": "test@test.ru",
            "password": "test",
            "tg_chat_id": "1",
        }
        # Неавторизован
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.json()["email"], "test@test.ru")
        # Авторизован
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 2)

    def test_user_detail(self):
        """Тест на просмотр профиля"""

        url = reverse("users:profile")
        data = {
            "id": self.user1.pk,
            "email": self.user1.email,
            "tg_chat_id": self.user1.tg_chat_id,
        }
        # Неавторизован
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Пользователь
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)

    def test_password_update(self):
        """Тест на смену пароля"""

        url = reverse("users:update-password")
        data = {"old_password": "1", "new_password": "123"}
        # Неавторизован
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Пользователь
        self.client.force_authenticate(user=self.user1)
        # Че-попало
        response = self.client.patch(url, {"1": "1"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"new_password": ["Обязательное поле."], "old_password": ["Обязательное поле."]}
        )
        # Неверный пароль
        response = self.client.patch(url, {"old_password": "0", "new_password": "123"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"old_password": "Неверный пароль"})
        # Верный пароль
        response = self.client.patch(url, {"old_password": "1", "new_password": "123"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Пароль успешно изменен"})
