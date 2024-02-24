Фриланс для репетиторов  
Этот проект предоставляет репетиторам API для просмотра и принятия заказов, сделанных пользователями. Пользователи могут размещать заказы на уроки и просматривать свободных репетиторов.  
Оглавление:  
1.[Используемый стек технологий](#используемый-стек-технологий)  
2.[Схема БД](#схема-бд)  
3.[Реализованная функциональность](#реализованная-функциональность)  
4.[Примеры API](#примеры-API)  
5.[Автор](#автор)  
## Используемый стек технологий:   
 • FastAPI  
 • SQLAlchemy  
 • PostgreSQL(asyncpg)  
 • Alembic  
 • Pytest(pytest-asyncio)  
 • Redis  
 • Celery  
 • Git  
## Схема БД 

## Реализованная функциональность:  
- Регистрация пользователей с разными правами. [Реализация](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/__init__.py#L29)
- Подтверждение почты пользователя. [Реализация](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/user/config.py#L40)    
- Работа с профилем(и) пользователя(ей) (профиль может создать только репетитор):  
  - CRUD (
    [удаление](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/profile/views.py#L56),
    [создание](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/profile/views.py#L20),
    [обновление](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/profile/views.py#L40),
    [чтение всего профиля](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/user/views.py#L54))
     профиля.  
  - Работа с предметами которые ведет репетитор ([удаление](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/user/views.py#L65), [добавление](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/user/views.py#L28))  
  - Получения предметов, которые он ведет. [Реализация](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/user/views.py#L41)  
- Получение всех репетиторов, которые ведут определенный предмет. [Реализация] (https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/user/views.py#L50)
- Работа с заказом (создать заказ может только заказчик):  
  - CRUD ([удаление](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/order/views.py#L58), [создание](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/order/views.py#L19), [чтение](https://github.com/kolyaslow/freelance_tutor/blob/master/api_v1/order/views.py#L34)) заказа.  
  - Получение всех заказов, которые репетитор может взять.  
## Примеры API:  
Получение всех заказов, которые репетитор может взять.   
Получение полного профиля репетитора.  
## Автор  
	



