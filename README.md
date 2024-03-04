## Фриланс для репетиторов
Этот проект представляет собой API, часть backend-приложения для просмотра и принятия заказов репетиторами.
## Оглавление

1. [Используемый стек технологий](#используемый-стек-технологий)
2. [Запуск и тестирование](#запуск-и-тестирование)
3. [Реализованная функциональность](#реализованная-функциональность)
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

## Запуск приложения:
Клонируйте репозиторий на локальную машину:
```commandline
$ git clone https://github.com/kolyaslow/freelance_tutor.git
```
Выполните команды Docker.
```docker
$ sudo docker compose up
```
## Реализованная функциональность
- Регистрация пользователей с разными правами. [Реализация.](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/user/config.py#L29)
- Подтверждение почты пользователя. [Реализация.](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/user/config.py#L40)
- Работа с профилем(ями) пользователя(ей) (профиль может создать только репетитор):
  - CRUD ([удаление](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/profile/views.py#L56),
    [создание](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/profile/views.py#L20),
    [обновление](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/profile/views.py#L40),
    [чтение всего профиля](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/user/views.py#L54))
     профиля.
  - Работа с предметами которые ведет репетитор. ([удаление](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/user/views.py#L65), [добавление](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/user/views.py#L28))
  - Получения предметов, которые ведет репетитор. [Реализация.](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/user/views.py#L41)
- Получение всех репетиторов, которые ведут определенный предмет. [Реализация.](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/user/views.py#L50)
- Работа с заказом (создать заказ может только заказчик):
  - CRUD ([удаление](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/order/views.py#L58), [создание](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/order/views.py#L19), [чтение](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/order/views.py#L34)) заказа.
  - Получение всех заказов, которые репетитор может взять. [Реализация.](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/order/views.py#L47)


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
|   |   |   mixins.py                       # Модуль примесей для создание связей между таблицами БД
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

После запуска интерактивная документация доступна по адресу:
```
http://127.0.0.1:8008/docs#/
```
Реализовано через OpenAPI(Swagger)

</details>


## Автор
**Николай Пышенко**
- email: pysenkon@gmail.com
- Telegram: [@koliaslow](https://t.me/koliaslow)
- VK: [@koliaslow](https://vk.com/koliaslow)
