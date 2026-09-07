# 📚 Library Service API
 
A REST API for managing a library: books catalog, users, and book borrowings — built with **Django** and **Django REST Framework**.
 
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-6.1-092E20?logo=django)
![DRF](https://img.shields.io/badge/DRF-REST_Framework-red)
![JWT](https://img.shields.io/badge/Auth-JWT-black)
 
---
 
## ✨ Features
 
- 🔑 **JWT authentication** (access / refresh / verify tokens)
- 👤 **Custom user model** with email as the login field
- 📖 **Books catalog** with search by title/author and admin-only editing
- 🔄 **Borrowings** — issue a book, return a book, track active/finished borrowings
- 📊 **Automatic inventory management** — a book's stock decreases on borrow and increases on return
- 🛡️ **Role-based permissions** — regular users see and manage only their own borrowings, staff see everything
- 📑 **Pagination** on list endpoints
- 🚦 **Rate limiting / throttling** for anonymous and authenticated users
- 📘 **Interactive API docs** via Swagger and Redoc (drf-spectacular)
---
 
## 🛠 Tech Stack
 
| Component        | Technology                        |
|-------------------|------------------------------------|
| Language          | Python 3                          |
| Framework         | Django 6.1                        |
| API               | Django REST Framework             |
| Auth              | Simple JWT (`rest_framework_simplejwt`) |
| API Documentation | drf-spectacular (Swagger / Redoc) |
| Database          | SQLite (dev) / PostgreSQL-ready   |
| Debugging         | Django Debug Toolbar              |
 
---
 
## 📂 Project Structure
 
```
Library_Service_API/
├── Library_service/     # Project settings, root URLs
├── books/                # Book catalog app
├── users/                # Custom user model, registration, JWT
├── borrowings/           # Borrowing logic (issue / return)
└── manage.py
```
 
---
 
## 🚀 Getting Started
 
### 1. Clone the repository
 
```bash
git clone <repository-url>
cd Library_Service_API
```
 
### 2. Create and activate a virtual environment
 
```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```
 
### 3. Install dependencies
 
```bash
pip install django djangorestframework djangorestframework-simplejwt drf-spectacular python-dotenv django-debug-toolbar
```
 
> 💡 It's recommended to freeze these into a `requirements.txt` for the project (`pip freeze > requirements.txt`).
 
### 4. Configure environment variables
 
Copy `.env.example` to `.env` and fill in your own values:
 
```bash
cp .env.example .env
```
 
```env
SECRET_KEY=your-secret-key
DEBUG=True
POSTGRES_DB=your_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```
 
### 5. Apply migrations
 
```bash
python manage.py migrate
```
 
### 6. Create a superuser (for admin access)
 
```bash
python manage.py createsuperuser
```
 
### 7. Run the development server
 
```bash
python manage.py runserver
```
 
The API will be available at **http://127.0.0.1:8000/**.
 
---
 
## 📘 API Documentation
 
| Endpoint                  | Description            |
|----------------------------|-------------------------|
| `/api/schema/`             | Raw OpenAPI schema      |
| `/api/doc/swagger/`        | Swagger UI              |
| `/api/doc/redoc/`          | Redoc UI                |
 
---
 
## 🔌 API Endpoints
 
### 👤 Users & Auth (`/api/users/`)
 
| Method | Endpoint               | Description                    | Access        |
|--------|-------------------------|---------------------------------|---------------|
| POST   | `/api/users/register/`  | Register a new user             | Public        |
| POST   | `/api/users/token/`     | Obtain JWT access/refresh pair | Public        |
| POST   | `/api/users/token/refresh/` | Refresh access token       | Public        |
| POST   | `/api/users/token/verify/`  | Verify a token              | Public        |
| GET/PUT/PATCH | `/api/users/me/` | View or update your own profile | Authenticated |
 
### 📖 Books (`/api/books/`)
 
| Method            | Endpoint          | Description                              | Access         |
|-------------------|-------------------|-------------------------------------------|----------------|
| GET                | `/api/books/`     | List books (filter by `?title=` / `?author=`) | Everyone       |
| GET                | `/api/books/{id}/`| Retrieve a single book                    | Everyone       |
| POST               | `/api/books/`     | Create a book                              | Staff only     |
| PUT/PATCH          | `/api/books/{id}/`| Update a book                              | Staff only     |
| DELETE             | `/api/books/{id}/`| Delete a book                              | Staff only     |
 
### 🔄 Borrowings (`/api/borrowings/`)
 
| Method | Endpoint                            | Description                                         | Access                        |
|--------|---------------------------------------|-------------------------------------------------------|-------------------------------|
| GET    | `/api/borrowings/`                    | List borrowings (filter by `?is_active=` / `?user_id=` for staff) | Authenticated (own records; staff see all) |
| GET    | `/api/borrowings/{id}/`               | Retrieve a borrowing                                  | Authenticated                 |
| POST   | `/api/borrowings/`                    | Borrow a book (decreases book inventory by 1)         | Authenticated                 |
| POST   | `/api/borrowings/{id}/return/`        | Return a borrowed book (increases inventory by 1)     | Owner or staff                |
 
---
 
## 🔐 Authentication
 
The API uses **JWT** authentication. After registering, obtain a token pair:
 
```http
POST /api/users/token/
{
  "email": "user@example.com",
  "password": "your-password"
}
```
 
Then include the access token in the `Authorize` request header for protected endpoints:
 
```
Authorize: Bearer <your-access-token>
```
 
> ⚠️ Note: this project uses a custom header name `AUTHORIZE` (instead of the default `Authorization`) for the JWT token, as configured in `SIMPLE_JWT`.
 
---
 
## 👥 User Roles
 
| Role           | Permissions                                                                 |
|-----------------|-------------------------------------------------------------------------------|
| **Anonymous**   | Browse the book catalog, register, obtain a token                            |
| **Authenticated user** | Manage own profile, borrow/return books, view own borrowing history    |
| **Staff / Admin**| Full access — manage books, view and manage all users' borrowings         |
 
---
 
## ✅ Running Tests
 
```bash
python manage.py test
```
 
Coverage report:
 
```bash
coverage run manage.py test
coverage report
```
 
---
 
## 📄 License
 
This project is available for educational and personal use. Add a license of your choice (MIT, Apache 2.0, etc.).
 
---
---
 
# 📚 Library Service API (Русская версия)
 
REST API для управления библиотекой: каталог книг, пользователи и выдача книг — построено на **Django** и **Django REST Framework**.
 
---
 
## ✨ Возможности
 
- 🔑 **JWT-аутентификация** (access / refresh / verify токены)
- 👤 **Кастомная модель пользователя** с входом по email
- 📖 **Каталог книг** с поиском по названию/автору и редактированием только для администраторов
- 🔄 **Выдача книг (borrowings)** — оформление и возврат книги, отслеживание активных/завершённых выдач
- 📊 **Автоматический учёт запасов** — количество экземпляров книги уменьшается при выдаче и увеличивается при возврате
- 🛡️ **Разграничение прав доступа** — обычные пользователи видят и управляют только своими выдачами, персонал видит всё
- 📑 **Пагинация** на списковых эндпоинтах
- 🚦 **Ограничение частоты запросов** для анонимных и авторизованных пользователей
- 📘 **Интерактивная документация API** через Swagger и Redoc (drf-spectacular)
---
 
## 🛠 Технологический стек
 
| Компонент          | Технология                          |
|----------------------|---------------------------------------|
| Язык                 | Python 3                              |
| Фреймворк            | Django 6.1                            |
| API                  | Django REST Framework                 |
| Авторизация          | Simple JWT (`rest_framework_simplejwt`) |
| Документация API     | drf-spectacular (Swagger / Redoc)     |
| База данных          | SQLite (для разработки) / готова к PostgreSQL |
| Отладка              | Django Debug Toolbar                  |
 
---
 
## 📂 Структура проекта
 
```
Library_Service_API/
├── Library_service/     # Настройки проекта, корневые URL
├── books/                # Приложение каталога книг
├── users/                # Кастомная модель пользователя, регистрация, JWT
├── borrowings/           # Логика выдачи книг (выдать / вернуть)
└── manage.py
```
 
---
 
## 🚀 Установка и запуск
 
### 1. Клонируйте репозиторий
 
```bash
git clone <repository-url>
cd Library_Service_API
```
 
### 2. Создайте и активируйте виртуальное окружение
 
```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```
 
### 3. Установите зависимости
 
```bash
pip install django djangorestframework djangorestframework-simplejwt drf-spectacular python-dotenv django-debug-toolbar
```
 
> 💡 Рекомендуется зафиксировать зависимости в `requirements.txt` (`pip freeze > requirements.txt`).
 
### 4. Настройте переменные окружения
 
Скопируйте `.env.example` в `.env` и заполните своими значениями:
 
```bash
cp .env.example .env
```
 
```env
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
POSTGRES_DB=ваша_база
POSTGRES_USER=ваш_пользователь
POSTGRES_PASSWORD=ваш_пароль
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```
 
### 5. Примените миграции
 
```bash
python manage.py migrate
```
 
### 6. Создайте суперпользователя (для доступа к админке)
 
```bash
python manage.py createsuperuser
```
 
### 7. Запустите сервер разработки
 
```bash
python manage.py runserver
```
 
API будет доступен по адресу **http://127.0.0.1:8000/**.
 
---
 
## 📘 Документация API
 
| Эндпоинт                  | Описание                |
|------------------------------|----------------------------|
| `/api/schema/`             | Исходная OpenAPI-схема    |
| `/api/doc/swagger/`        | Swagger UI                |
| `/api/doc/redoc/`          | Redoc UI                  |
 
---
 
## 🔌 Эндпоинты API
 
### 👤 Пользователи и авторизация (`/api/users/`)
 
| Метод  | Эндпоинт                     | Описание                             | Доступ         |
|--------|---------------------------------|-----------------------------------------|-----------------|
| POST   | `/api/users/register/`         | Регистрация нового пользователя        | Публичный       |
| POST   | `/api/users/token/`            | Получить пару access/refresh токенов   | Публичный       |
| POST   | `/api/users/token/refresh/`    | Обновить access-токен                  | Публичный       |
| POST   | `/api/users/token/verify/`     | Проверить токен                        | Публичный       |
| GET/PUT/PATCH | `/api/users/me/`        | Просмотр/изменение своего профиля      | Авторизован     |
 
### 📖 Книги (`/api/books/`)
 
| Метод              | Эндпоинт           | Описание                                     | Доступ          |
|---------------------|----------------------|--------------------------------------------------|------------------|
| GET                  | `/api/books/`       | Список книг (фильтры `?title=` / `?author=`)     | Все              |
| GET                  | `/api/books/{id}/`  | Получить одну книгу                               | Все              |
| POST                 | `/api/books/`       | Создать книгу                                     | Только персонал  |
| PUT/PATCH            | `/api/books/{id}/`  | Обновить книгу                                    | Только персонал  |
| DELETE               | `/api/books/{id}/`  | Удалить книгу                                     | Только персонал  |
 
### 🔄 Выдача книг (`/api/borrowings/`)
 
| Метод | Эндпоинт                              | Описание                                                     | Доступ                                  |
|-------|------------------------------------------|-------------------------------------------------------------------|-------------------------------------------|
| GET   | `/api/borrowings/`                      | Список выдач (фильтры `?is_active=` / `?user_id=` для персонала) | Авторизован (свои записи; персонал — все) |
| GET   | `/api/borrowings/{id}/`                 | Получить одну выдачу                                              | Авторизован                               |
| POST  | `/api/borrowings/`                      | Выдать книгу (уменьшает запас на 1)                               | Авторизован                               |
| POST  | `/api/borrowings/{id}/return/`          | Вернуть книгу (увеличивает запас на 1)                            | Владелец или персонал                     |
 
---
 
## 🔐 Аутентификация
 
API использует **JWT**-аутентификацию. После регистрации получите пару токенов:
 
```http
POST /api/users/token/
{
  "email": "user@example.com",
  "password": "ваш-пароль"
}
```
 
Затем добавляйте access-токен в заголовок запроса `Authorize` для защищённых эндпоинтов:
 
```
Authorize: Bearer <ваш-access-токен>
```
 
> ⚠️ Обратите внимание: в проекте используется кастомное имя заголовка `AUTHORIZE` (вместо стандартного `Authorization`) для передачи JWT-токена — это настроено в `SIMPLE_JWT`.
 
---
 
## 👥 Роли пользователей
 
| Роль                  | Права доступа                                                                 |
|-------------------------|-----------------------------------------------------------------------------------|
| **Аноним**             | Просмотр каталога книг, регистрация, получение токена                            |
| **Авторизованный пользователь** | Управление своим профилем, выдача/возврат книг, просмотр своей истории выдач |
| **Персонал / Админ**  | Полный доступ — управление книгами, просмотр и управление выдачами всех пользователей |
 
---
 
## ✅ Запуск тестов
 
```bash
python manage.py test
```
 
Отчёт о покрытии:
 
```bash
coverage run manage.py test
coverage report
```
 
---
 
## 📄 Лицензия
 
Проект доступен для учебного и личного использования. Добавьте лицензию по своему усмотрению (MIT, Apache 2.0 и т.д.).
 

