![Python](https://img.shields.io/badge/Python-3.10-blue)
![Django](https://img.shields.io/badge/Django-4.2-brightgreen)
![DRF](https://img.shields.io/badge/DRF-3.15-gray)
![Redis](https://img.shields.io/badge/Redis-5.1-red)
![Celery](https://img.shields.io/badge/Celery-5.4-green)

# Atomic-habits (Атомные привычки)

В 2018 году Джеймс Клир написал книгу «Атомные привычки», которая посвящена приобретению новых полезных привычек и искоренению старых плохих привычек. Заказчик прочитал книгу, впечатлился и обратился с запросом реализовать трекер полезных привычек.

## Основные характеристики проекта:

- **RESTful API**: Используемый **Django REST Framework** обеспечивает создание гибкого и масштабируемого API для взаимодействия между клиентом и сервером.
- **JWT-аутентификация**: Для безопасной аутентификации пользователей используется **djangorestframework-simplejwt**.
- **Telegram API**: Интегрирован телеграм-бот для сообщения пользователю о выполении задачи.
- **Celery-beat**: Используется для асинхронной обработки задач, а именно отправка сообщения телеграм-ботом, задействован django-celery.
- **CORS (Cross-Origin Resource Sharing)**: Настраивается для разрешения запросов на API с разных источников, что необходимо для работы с фронтенд-приложениями и мобильными приложениями.
- **Документация API**: Интерактивная документация API реализована с помощью **drf-yasg**, что облегчает тестирование и использование API.

## 🛠️ Установка

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/troxin-a/atomic-habits.git
cd atomic-habits
```

2. **Создайте файл .env в корневом каталоге проекта и добавьте необходимые переменные окружения:**

```bash
cp .env.sample .env
nano .env
```

3. **Запустите docker-compose файл:**

```bash
docker compose up -d --build
```

4. **Примените миграции:**

```bash
docker compose exec app python manage.py migrate
```

5. **Создайте суперпользователя:**

```bash
docker compose exec app python manage.py csu
```

## 📚️ Использование
Документация по использованию API будет доступна после запуска сервера по ссылке: http://127.0.0.1:8000/redoc/ или http://127.0.0.1:8000/swagger/
