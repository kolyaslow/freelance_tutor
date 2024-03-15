## Фриланс для репетиторов
Этот проект представляет собой API, часть backend-приложения для просмотра и принятия заказов репетиторами. В проекте реализовано:
- Различные виды связи в БД;
- Интеграция со стороним API;
- Взаимодействие между пользователями;
- Права доступа к API.
## Оглавление

1. [Используемый стек технологий](#используемый-стек-технологий)
2. [Запуск](#запуск)
3. [Тестирование](#тестирование)
4. [Документация](#Документация)
5. [Автор](#автор)

## Используемый стек технологий
- FastAPI
- SQLAlchemy
- PostgreSQL(asyncpg)
- Alembic
- Pytest(pytest-asyncio)
- Redis
- Celery
- Git
- Docker

## Запуск:
Клонируйте репозиторий на локальную машину:
```commandline
$ git clone https://github.com/kolyaslow/freelance_tutor.git
```
Выполните команды Docker.
```docker
$ sudo docker compose up
```

## Тестирование:
Выполните команды Docker.
```docker
$ sudo docker compose exec app pytest -s -v
```

## Документация

<details>
<summary>Схема БД</summary>

![photo](/photo/db.png)

>Сущность User
```
id(PK) - уникальный идентификатор записи
email - email пользователя указанный при регистрации
hashed_password - хэш пароля
is_active - показатель, что пользователь пользуется аккаунтом
is_superuser - поле показывающее, что пользователь суперпользователь
is_verified - поле показывающее, что пользователь подтвердил email
role - роль пользователя (репетитор, ученик)
```

>Сущность Profile
```
id(PK) - уникальный идентификатор записи
fullname - ФИО репетитора
description - описание профиля
```

>Сущность Subject
```
name(PK) - название предмета
```

>Сущность SubjectUserAssociation
```
id(PK) - уникальный идентификатор записи
user_id(FK) - id пользователя (репетитора)
subject_name(FK) - название предмета
```

>Сущность Order
```
id(PK) - уникальный идентификатор записи
user_id(FK) - id пользователя (ученика)
subject_name(FK) - название предмета
description - описание профиля
is_active - поле показывающее, открыт ли заказ или закрыт
```

>Сущность Response
```
id(PK) - уникальный идентификатор записи
order_id(FK) - id заказа
user_id(FK) - id пользователя (репетитора)
status - показатель принятие репетитора, как исполнителя
```

>Сущность ConfirmationKeys
```
id(PK) - уникальный идентификатор записи
user_id(FK) - id пользователя (репетитора)
email_confirmation_code - код подтверждения email пользователя
```
</details>

<details>

<summary>Схема проекта</summary>

```commandline
|   main.py             # Точка входа проекта
|   pyproject.toml      # Зависимости проекта
|
+---alembic     # Модуль миграции БД
+---api_v1      # Модуль API_V1
|   |   schemas_confirmation_keys.py    # Pydentic схемы для таблицы confirmation_keys
|   |   __init__.py                     # Инициализатор пакета, где все роутеры собираются для последуещего импорта в экземпляр fastapi(app)
|   |
|   +---common  # Модуль с общими функциями необходимыми API
|   |   |   crud.py                     # Модуль для взаимодействия с базой данных
|   |   |   dependencies.py             # Модуль для описания зависимостей
|   |
|   +---order
|   |   |   crud.py
|   |   |   dependencies.py
|   |   |   schemas.py
|   |   |   views.py        # Модуль для описание endpoint API
|   |
|   +---profile
|   |   |   crud.py
|   |   |   dependencies.py
|   |   |   schemas.py
|   |   |   views.py
|   |
|   +---subject
|   |   |   crud.py
|   |   |   dependencies.py
|   |   |   schemas.py
|   |   |   views.py
|   |
|   +---task_selery
|   |   |   config.py       # Конфигурация даных для модуля
|   |   |   send_email.py   # Модуль отправки письма на email
|   |
|   +---user
|   |   |   config.py
|   |   |   crud.py
|   |   |   fastapi_user.py     # Модуль создания экземпляра FastapiUser
|   |   |   schemas.py
|   |   |   views.py
|   |
+---core
|   |   config.py           # Конфигурация проекта, в том числе, бд
|   |   db_helper.py        # Создание AsyncEngine, AsycSessionFactory
|   |   __init__.py
|   |
|   +---models
|   |   |   base.py                         # Модуль базовой модели ORM
|   |   |   confirmation_keys.py
|   |   |   mixins.py                       # Модуль примесей для создания связей между таблицами БД
|   |   |   order.py
|   |   |   profile.py
|   |   |   subject.py
|   |   |   subject_user_association.py     # Таблица для связи "многие-ко-многим" между таблицами subject и user
|   |   |   user.py
|   |   |   __init__.py                     # Инициализация всех элементов для работы с БД через SQLalchemy.
+---tests   # Модуль с тестами проекта
|   |   conftest.py       # Общие фикстуры необходимые тестам
|   |   test_inaccessibility_api.py     # Тесты проверки авторизации API
|   |
|   +---common
|   |   |   base_request_api.py     # Модуль формирования и оправки тестовых запросов
|   |   |   fixture_profile_management.py       # Модуль фикстур, отвечающих за управление профилем
|   |   |   subject_fixture.py
|   |   |   user_authentication_fixture.py      # Модуль аутентификации пользователей с разными правами
|   |   |   __init__.py
|   |
|   +---order
|   |   |   conftest.py
|   |   |   test_router_create_order.py     # Тесты для роутера create_order
|   |   |   test_router_delete_order.py
|   |   |   test_router_getting_orders_for_tutor.py
|   |   |   test_router_get_all_orders.py
|   |
|   +---profile
|   |   |   test_router_create.py
|   |   |   test_router_delete.py
|   |   |   test_router_update.py
|   |
|   +---user
|   |   |   test_router_get_subjects_by_user.py
|   |   |   test_router_show_all_tutor_by_subject.py
|   |
```
</details>

<details>

<summary>Описание API</summary>

После запуска интерактивная документация доступна по адресу (Реализовано через OpenAPI(Swagger)):
```
http://127.0.0.1:8008/docs#/
```
Все API, кроме API аутентификации, доступны *только* аутентифицированным пользователем,
которые подтвердили свою почту
  <details>

  <summary>Регистрация пользователя</summary>
    Регистрирует пользователя в системе, а также отправляет письмо с кодом подтверждения на указанный при регистрации email.

- Запрос:

```
/auth/register
```
- Тело запроса:
```json
{
  "email": "user@example.com", # email пользователя
  "password": "string", # пароль
  "role": "tutor" # роль соответствующая значениям tutor или customer
}
```
- Тело ответа:
```json
{
  "id": 16,   # id записи в БД
  "email": "use4r@example.com",   # email указанный при регистрации
  "is_active": true,    # показатель блокировки пользователя, всегда проставляется в значение True
  "is_superuser": false,    # суперпользователь, всегда проставляется в значение False
  "is_verified": false,   # показатель подтверждения почты пользователем
  "role": "tutor"   # роль указанная при регистрации
}
```
- Ошибка повторной регистрации пользователя, код ошибки 400:
```json
{
  "detail": "REGISTER_USER_ALREADY_EXISTS"
}
```

  </details>

<details>

  <summary>Подтвердение почты</summary>
Проверка кода подтверждения отправленного при регистрации и установка поля is_verified=True,
при неверном указании почты исключение не выкидывается. При успешном подтверждении вернется статус код 200, при неверном 401.

- Запрос:

```
/user/verify_user?user_email=user%40example.com.com&code=asdas

user_email - email указанный при регистрации
code - код подтверждления отправленный на почту
```
  </details>

<details>

  <summary>API для работы с профилем</summary>

API доступно лишь репетиторам.
При попытке получить доступ не репетитором вызывает исключение. см. [общие исключения](#общие_исключения)
  <details>

  <summary>Создание профиля</summary>

Создание профиля для репетиторов. Все параметры являются необязательными.

- Запрос:
```
/profile/create_profile
```
- Тело запроса:
```json
{
  "fullname": "string", # необязательный параметр, полное имя пользователя
  "description": "string",    # необязательный параметр, описание профиля
  "user_id": 0    # id пользователя, заполняется автоматически
}

```

- Тело ответа:
```json
{
  "fullname": "string",   # полное имя пользователя, указанного при создании профиля
  "description": "string"   # описание, указанное при создании профиля
}
```

- Ошибка повторного создания профиля, статус код 422:
```json
{
  "detail": "Профиль для пользователя с именем user@example.com уже создан",
}
```

</details>

  <details>

  <summary>Обновление профиля</summary>

Запрос позволяет обновить профиль репетитора. Все параметры необязательны для заполнения.
- Запрос:
```json
/profile/update_profile
```
- Тело запроса:
```json
{
  "fullname": "string",   # необязательный параметр, ФИО пользователя
  "description": "string"   # необязательный параметр, описание проекта
}
```
- Тело ответа:
```json
{
  "fullname": "string",   # ФИО, указанное при обновлении
  "description": "string", # описание, указанное при обновлнеи
  "user_id": 0    # id пользователя, репетитора
}
```
</details>

<details>

  <summary>Удаление профиля</summary>

Удаление профиля репетитора. При успешном удалении возвращается статус код 204.

- Запрос:
```json
/profile/delete_profile
```
- Ошибка удаление несуществующего профиля, статус код 404:

```json
{
  "detail": "No profile was found for user user@gmail.com"
}

```

</details>

<details>
  <summary>Добавление предметов, которые ведет репетитор</summary>

Добавление в профиль предметов, которые репетитор может вести.
При успешном добавлении вернется статус код 200.

- Запрос:
```
/user/add_subject
```

Тело запроса:
```json
[
  "name_subject"    # название предмета, соответсвующее предметам из таблици Subject
]
```


</details>

</details>

<details>
  <summary>API для работы с заказом</summary>

  API доступны лишь пользователям, являющиеся заказчиками, т.е. поле `role=customer`.
  При попытке получить доступ не заказчикам вызывает исключение см. [общие исключения](#общие_исключения)

  <details>

<summary>Создание заказа</summary>
  Создание заказа, при повторном создании заказа, исключение не выкидывается.

- Запрос:

```json
/order/create_order
```

Тело запроса:

```json
{
  "description": "string",    # описание заказа
  "is_active": true,    # готовность получать отклики на заказ, обциональный параметр, дефолное значение true,
  "subject_name": "mathematics", # предмет соответсвующий значениям таблици subject
  "user_id": 0    # id заказчика, заполняется автоматически
}
```
- Тело ответа:

```json
{
  "description": "string",
  "is_active": true,
  "subject_name": "mathematics",
  "user_id": 0,
  "id": 0   # id заказа
}
```

</details>
    <details>

<summary>Получение всех заказов заказчиком</summary>

Получение всех заказов, которые создал закзачик. При отсутсвии заказавов, вернет пустой список.

- Запрос:

```json
/order/get_all_orders
```
- Тело ответа:
```json
[
  {
    "description": "string",
    "is_active": true,
    "subject_name": "mathematics",
    "user_id": 0,   # id заказчика
    "id": 0
  },
]
```
</details>

<details>

<summary>Получение всех заказов для репетитора</summary>

Получение всех заказов, которые репетитор может вести,
то есть предметы в заказе и те, что ведет репетитор совпадают, а также закза открыт для откликов
(поле заказа is_active=True )
При отсутсвии заказов, вернется пустой список.

- Запрос:
```
/order/getting_orders_for_tutor?page=0&size=10

page - необязательный параметр, дефолтное значение 0, страница погинации
size - необязательный параметр, дефолтное значение 10, количество элементов на странице
```

- Тело ответа:
```json
[
  {
    "description": "string",    # описание заказа
    "is_active": true,    # открыт ли заказа, для откликов
    "subject_name": "mathematics",  # предмет, который требуется проводить
    "user_id": 0  # id заказачика
  }
]
```
</details>
<details>

<summary>Удаление заказа</summary>

При успешном удалении заказа, вернется код 204.
- Запрос:
```
/order/delete_order/id_order

id_order: int - id заказа
```

- Ошибка удаления несуществующего закза, статус код 404:
```json
{
  "detail": "Незвозможно получить объект по его id"
}
```

</details>
</details>


<details>

  <summary> Просмотр репетиторов</summary>
Получения списка репетиторов по опредленному предмету, если таких репетиторов нет, вернет пустой список.

- Запрос:
```
/user/show_all_tutor_by_subject/name_subject?page=0&size=10

name_subject: str - название предмета, соответсвующее предметам из таблицы Subject
page - обциональный параметр страницы пагинации, дефолтнрое значение 0
size - обциональный параметр количетво элемнтов, дефолтнрое значение 10
```

- Тело ответа:
```json
]
  {
    "fullname": "string", # ФИО репетитора
    "description": "string" # описание профиля репетитора
  },
]
```

</details>
<details>

  <summary id="общие_исключения">Общие исключения</summary>

- Ошибка валидации, статус код 422:

```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

```
- Ошибка недоступности API, статус код 401:
```json
{
  "detail": "Unauthorized"
}
```
</details>

</details>


## Автор
**Николай Пышенко**
- email: pysenkon@gmail.com
- Telegram: [@koliaslow](https://t.me/koliaslow)
- VK: [@koliaslow](https://vk.com/koliaslow)
