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
- **Celery-beat**: Для выполнения периодических задач, а именно отправка сообщения телеграм-ботом, задействован django-celery-beat.
- **Документация API**: Интерактивная документация API реализована с помощью **drf-yasg**, что облегчает тестирование и использование API.

## 🛠️ Установка

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/troxin-a/edu-sphere.git
cd edu-sphere
```

2. **Активируйте виртуальное окружение:**

```bash
poetry shell
```

3. **Установите зависимости:**

```bash
poetry install
```

4. **Создайте базу данных и примените миграции:**

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

5. **Создайте файл .env в корневом каталоге проекта и добавьте необходимые переменные окружения:**

```bash
cp .env.sample .env
nano .env
```

6. **Создайте группу модераторов приложение auth для создания необходимых групп пользователей:**

```bash
python3 manage.py fill
```

7. **Создайте суперпользователя:**

```bash
python3 manage.py csu
```

8. **Запустите локальный сервер:**

```bash
python3 manage.py runserver
```

9. **Запустите redis на локальной машине:**

```bash
redis-server
```

10. **Запустите celery + celery-beat:**

```bash
celery -A config worker --beat --scheduler django --loglevel=info
```

## 📚️ Использование
Документация по использованию API будет доступна после запуска сервера по ссылке: http://127.0.0.1:8000/redoc/
