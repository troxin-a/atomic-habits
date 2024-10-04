from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from habits.models import Habit

from config.settings import REST_FRAMEWORK


non_field = REST_FRAMEWORK["NON_FIELD_ERRORS_KEY"]


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(email="user1@test.ru")
        self.user2 = User.objects.create(email="user2@test.ru")
        self.nice_habit = Habit.objects.create(
            user=self.user1,
            place="Приятная привычка",
            time="12:00:00",
            doing="Приятная привычка",
            duration=1,
            nice=True,
            is_published=True,
        )
        self.health_habit1 = Habit.objects.create(
            user=self.user1,
            place="Полезная привычка1",
            time="12:00:00",
            doing="Полезная привычка1",
            duration=1,
            related_habit=self.nice_habit,
            is_published=True,
        )
        self.health_habit2 = Habit.objects.create(
            user=self.user1,
            place="Полезная привычка2",
            time="12:00:00",
            doing="Полезная привычка2",
            duration=1,
            reward="Награда",
        )
        self.health_habit3 = Habit.objects.create(
            user=self.user2,
            place="Полезная привычка3",
            time="12:00:00",
            doing="Полезная привычка3",
            duration=1,
            reward="Награда",
        )

        self.valid_fail = [
            "Обязательно нужно указать одно из полей: related_habit, reward, nice",
            "related_habit, reward, nice: взаимоисключающие поля",
            "duration: Введите число от 1 до 120",
            "periodicity: Введите число от 1 до 7",
            f"related_habit: У вас недостаточно прав на объект {self.health_habit3.pk}",
            f"related_habit: Поле 'nice' у объекта {self.health_habit1.pk} должно быть 'True'",
        ]

    def test_habit_create(self):
        """Тест на создание привычки"""

        url = reverse("habits:list-create")
        data = {
            "place": "тест",
            "time": "12:00:00",
            "doing": "тест",
        }

        habit = {
            "doing": "тест",
            "duration": 5,
            "id": 5,
            "is_published": False,
            "nice": False,
            "periodicity": 3,
            "place": "тест",
            "related_habit": 1,
            "reward": "",
            "time": "12:00:00",
            "user": 1,
        }

        # Неавторизован
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Авторизован
        self.client.force_authenticate(user=self.user1)

        ## Пустые поля
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        ## Поля заполнены в соответствии с валидацией на уровне полей
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[non_field], [self.valid_fail[0]])

        ## Различные комбинации между related_habit, reward, nice
        response = self.client.post(
            url, dict(list(data.items()) + list({"related_habit": 1, "reward": "тест", "nice": True}.items()))
        )
        self.assertEqual(response.json()[non_field], [self.valid_fail[1]])
        response = self.client.post(url, dict(list(data.items()) + list({"reward": "тест", "nice": True}.items())))
        self.assertEqual(response.json()[non_field], [self.valid_fail[1]])
        response = self.client.post(url, dict(list(data.items()) + list({"related_habit": 1, "nice": True}.items())))
        self.assertEqual(response.json()[non_field], [self.valid_fail[1]])
        response = self.client.post(
            url, dict(list(data.items()) + list({"related_habit": 1, "reward": "тест"}.items()))
        )
        self.assertEqual(response.json()[non_field], [self.valid_fail[1]])
        response = self.client.post(url, dict(list(data.items()) + list({"related_habit": 2}.items())))
        self.assertEqual(response.json()[non_field], [self.valid_fail[5]])
        response = self.client.post(url, dict(list(data.items()) + list({"related_habit": 4}.items())))
        self.assertEqual(response.json()[non_field], [self.valid_fail[4]])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        ## Проверка на валидацию duration и periodicity
        response = self.client.post(url, dict(list(data.items()) + list({"related_habit": 1, "duration": -1}.items())))
        self.assertEqual(response.json()[non_field], [self.valid_fail[2]])
        response = self.client.post(url, dict(list(data.items()) + list({"related_habit": 1, "duration": 0}.items())))
        self.assertEqual(response.json()[non_field], [self.valid_fail[2]])
        response = self.client.post(
            url, dict(list(data.items()) + list({"related_habit": 1, "duration": 121}.items()))
        )
        self.assertEqual(response.json()[non_field], [self.valid_fail[2]])
        response = self.client.post(
            url, dict(list(data.items()) + list({"related_habit": 1, "periodicity": 8}.items()))
        )
        self.assertEqual(response.json()[non_field], [self.valid_fail[3]])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 4)

        ## Успешное создание объекта
        response = self.client.post(url, habit)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), habit)

    def test_habit_list(self):
        """Тест на список собственных"""

        url = reverse("habits:list-create")

        results = [
            {
                "doing": self.health_habit3.doing,
                "duration": self.health_habit3.duration,
                "id": self.health_habit3.id,
                "is_published": self.health_habit3.is_published,
                "nice": self.health_habit3.nice,
                "periodicity": self.health_habit3.periodicity,
                "place": self.health_habit3.place,
                "related_habit": self.health_habit3.related_habit,
                "reward": self.health_habit3.reward,
                "time": self.health_habit3.time,
                "user": self.health_habit3.user.id,
            }
        ]

        # Неавторизован
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Авторизован
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"], results)

    def test_habit_public_list(self):
        """Тест на список публичных"""

        url = reverse("habits:list-public")

        # Неавторизован
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Авторизован
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 2)

    def test_habit_update(self):
        """Тест на редактирование привычки"""

        url1 = reverse("habits:retrieve-update-destroy", args=(self.health_habit1.pk,))
        url2 = reverse("habits:retrieve-update-destroy", args=(self.health_habit3.pk,))

        habit = {
            "doing": self.health_habit1.doing,
            "duration": self.health_habit1.duration,
            "id": self.health_habit1.id,
            "is_published": self.health_habit1.is_published,
            "nice": self.health_habit1.nice,
            "periodicity": self.health_habit1.periodicity,
            "place": self.health_habit1.place,
            "related_habit": self.health_habit1.related_habit.id,
            "reward": self.health_habit1.reward,
            "time": self.health_habit1.time,
            "user": self.health_habit1.user.id,
        }

        # Неавторизован
        response = self.client.patch(url1, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Авторизован
        self.client.force_authenticate(user=self.user1)

        ## Пустые поля
        response = self.client.patch(url1, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), habit)

        ## Различные комбинации между related_habit, reward, nice
        response = self.client.patch(
            url1, {"related_habit": self.nice_habit.pk, "reward": "тест", "nice": True}, format="json"
        )
        self.assertEqual(response.json()[non_field], [self.valid_fail[1]])
        response = self.client.patch(url1, {"reward": "тест", "nice": True}, format="json")
        self.assertEqual(response.json()[non_field], [self.valid_fail[1]])
        response = self.client.patch(url1, {"nice": True}, format="json")
        self.assertEqual(response.json()[non_field], [self.valid_fail[1]])
        response = self.client.patch(url1, {"reward": "тест"}, format="json")
        self.assertEqual(response.json()[non_field], [self.valid_fail[1]])
        response = self.client.patch(url1, {"related_habit": self.nice_habit.pk, "nice": True}, format="json")
        self.assertEqual(response.json()[non_field], [self.valid_fail[1]])
        response = self.client.patch(url1, {"related_habit": self.nice_habit.pk, "reward": "тест"}, format="json")
        self.assertEqual(response.json()[non_field], [self.valid_fail[1]])
        response = self.client.patch(url1, {"related_habit": self.health_habit1.pk}, format="json")
        self.assertEqual(response.json()[non_field], [self.valid_fail[5]])
        response = self.client.patch(url1, {"related_habit": self.health_habit3.pk}, format="json")
        self.assertEqual(response.json()[non_field], [self.valid_fail[4]])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.patch(url1, {"nice": True, "related_habit": None}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.patch(url1, {"nice": False, "reward": "тест"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ## Изменени чужого объекта
        response = self.client.patch(url2, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_habit_delete(self):
        """Тест на удаление привычки"""

        url1 = reverse("habits:retrieve-update-destroy", args=(self.health_habit1.pk,))
        url2 = reverse("habits:retrieve-update-destroy", args=(self.health_habit3.pk,))
        url3 = reverse("habits:retrieve-update-destroy", args=(self.nice_habit.pk,))

        # Неавторизован
        response = self.client.delete(url1, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Авторизован
        self.client.force_authenticate(user=self.user1)
        # Удаление защищенного элемента (на него ссылаются другие объекты)
        response = self.client.delete(url3, format="json")
        self.assertEqual(response.status_code, status.HTTP_418_IM_A_TEAPOT)
        # Успешное удаление
        response = self.client.delete(url1, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Повторное удаление защищенного элемента (на него перестали ссылаться)
        response = self.client.delete(url3, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Удаление чужой привычки
        response = self.client.delete(url2, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
