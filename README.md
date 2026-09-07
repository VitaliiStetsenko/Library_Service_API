# 📚 Library Service API
 
A REST API for managing a library: books catalog, users, book borrowings, and **online payments** — built with **Django** and **Django REST Framework**.
 
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-6.1-092E20?logo=django)
![DRF](https://img.shields.io/badge/DRF-REST_Framework-red)
![JWT](https://img.shields.io/badge/Auth-JWT-black)
![Stripe](https://img.shields.io/badge/Payments-Stripe-635BFF?logo=stripe)
 
---
 
## ✨ Features
 
- 🔑 **JWT authentication** (access / refresh / verify tokens)
- 👤 **Custom user model** with email as the login field
- 📖 **Books catalog** with search by title/author and admin-only editing
- 🔄 **Borrowings** — issue a book, return a book, track active/finished borrowings
- 📊 **Automatic inventory management** — a book's stock decreases on borrow and increases on return
- 💳 **Stripe payments** — a checkout session is created automatically for every borrowing, plus automatic **overdue fines** when a book is returned late
- 🛡️ **Role-based permissions** — regular users see and manage only their own borrowings/payments, staff see everything
- 📑 **Pagination** on list endpoints
- 🚦 **Rate limiting / throttling** for anonymous and authenticated users
- 📘 **Interactive API docs** via Swagger and Redoc (drf-spectacular)
- ✅ **Test suite with coverage reporting** for the core apps (see [Testing](#-testing) below)
---
 
## 🛠 Tech Stack
 
| Component        | Technology                              |
|-------------------|-------------------------------------------|
| Language          | Python 3                                  |
| Framework         | Django 6.1                                |
| API               | Django REST Framework                     |
| Auth              | Simple JWT (`rest_framework_simplejwt`)   |
| Payments          | Stripe (`stripe` Python SDK)              |
| API Documentation | drf-spectacular (Swagger / Redoc)         |
| Database          | SQLite (dev) / PostgreSQL-ready           |
| Testing           | Django `TestCase` + `coverage.py`         |
| Debugging         | Django Debug Toolbar                      |
| Linting           | flake8                                    |
 
---
 
## 📂 Project Structure
 
```
Library_Service_API/
├── Library_service/     # Project settings, root URLs
├── books/                # Book catalog app (+ tests)
├── users/                # Custom user model, registration, JWT
├── borrowings/           # Borrowing logic: issue / return (+ tests)
├── payment/              # Stripe checkout sessions, fines, payment status
├── requirements.txt
├── manage.py
└── .env.example
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
pip install -r requirements.txt
```
 
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
 
# Stripe
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxxx
 
PAYMENT_SUCCESS_URL=http://localhost:3000/payment/success
PAYMENT_CANCEL_URL=http://localhost:3000/payment/cancel
FINE_MULTIPLIER=2
```
 
> 💳 You'll need a free [Stripe](https://dashboard.stripe.com/register) account and its **test-mode** API keys to try out the payment flow locally.
 
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
 
| Method | Endpoint                            | Description                                                          | Access                                     |
|--------|---------------------------------------|-------------------------------------------------------------------------|-----------------------------------------------|
| GET    | `/api/borrowings/`                    | List borrowings (filter by `?is_active=` / `?user_id=` for staff)      | Authenticated (own records; staff see all)    |
| GET    | `/api/borrowings/{id}/`               | Retrieve a borrowing                                                     | Authenticated                                 |
| POST   | `/api/borrowings/`                    | Borrow a book — decreases inventory by 1 and creates a Stripe payment session | Authenticated                            |
| POST   | `/api/borrowings/{id}/return/`        | Return a book — increases inventory by 1; if overdue, creates a **fine** payment session | Owner or staff                    |
 
### 💳 Payments (`/api/payments/`)
 
| Method | Endpoint                     | Description                                                        | Access                       |
|--------|--------------------------------|------------------------------------------------------------------------|-------------------------------|
| GET    | `/api/payments/`               | List payments (own only; staff see all)                                | Authenticated                 |
| GET    | `/api/payments/{id}/`          | Retrieve a payment                                                      | Owner or staff                |
| GET    | `/api/payments/success/?session_id=` | Confirm a Stripe checkout session and mark the payment as **PAID** | Public (called by Stripe redirect) |
| GET    | `/api/payments/cancel/`        | Notify that a checkout session was cancelled                           | Public (called by Stripe redirect) |
 
**How payments work:**
1. When a borrowing is created, a Stripe **Checkout Session** is generated automatically for the book's daily fee, and a `Payment` record (`status=PENDING`, `type=PAYMENT`) is linked to it.
2. The user completes the payment via the returned `session_url`; Stripe redirects them to `/api/payments/success/` or `/api/payments/cancel/`.
3. If a book is returned **after** its `expected_return_date`, a second Stripe session is created automatically for the calculated **fine** (`type=FINE`), using `daily_fee × days_overdue × FINE_MULTIPLIER`.
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
 
| Role           | Permissions                                                                                          |
|-----------------|----------------------------------------------------------------------------------------------------------|
| **Anonymous**   | Browse the book catalog, register, obtain a token                                                       |
| **Authenticated user** | Manage own profile, borrow/return books, view own borrowings and payments                        |
| **Staff / Admin**| Full access — manage books, view and manage all users' borrowings and payments                        |
 
---
 
## ✅ Testing
 
The project ships with a dedicated test suite built on Django's `TestCase`, covering the main business logic:
 
- **`books/tests.py`** — book CRUD, filtering by title/author, and permission checks (staff vs. read-only users)
- **`borrowings/tests.py`** — the most thoroughly covered module: creating a borrowing, inventory updates, the `return` action, overdue-fine calculation, and access control (own borrowings vs. staff-wide access)
- **`users/tests.py`** and **`payment/tests.py`** — basic smoke tests, with room to expand
Run the full test suite:
 
```bash
python manage.py test
```
 
Run tests with a coverage report:
 
```bash
coverage run manage.py test
coverage report
```
 
Generate an HTML coverage report (opens as `htmlcov/index.html`):
 
```bash
coverage html
```
 
> 📈 The repository already includes a generated `htmlcov/` report and a `.coveragerc` config, so you can inspect current coverage without re-running tests.
 
---
 
## 📄 License
 
This project is available for educational and personal use. Add a license of your choice (MIT, Apache 2.0, etc.).
 
---
---
 
# 📚 Library Service API (Русская версия)
 
REST API для управления библиотекой: каталог книг, пользователи, выдача книг и **онлайн-оплата** — построено на **Django** и **Django REST Framework**.
 
---
 
## ✨ Возможности
 
- 🔑 **JWT-аутентификация** (access / refresh / verify токены)
- 👤 **Кастомная модель пользователя** с входом по email
- 📖 **Каталог книг** с поиском по названию/автору и редактированием только для администраторов
- 🔄 **Выдача книг (borrowings)** — оформление и возврат книги, отслеживание активных/завершённых выдач
- 📊 **Автоматический учёт запасов** — количество экземпляров книги уменьшается при выдаче и увеличивается при возврате
- 💳 **Оплата через Stripe** — при каждой выдаче книги автоматически создаётся сессия оплаты, а при просрочке возврата — автоматически начисляется **штраф**
- 🛡️ **Разграничение прав доступа** — обычные пользователи видят и управляют только своими выдачами/платежами, персонал видит всё
- 📑 **Пагинация** на списковых эндпоинтах
- 🚦 **Ограничение частоты запросов** для анонимных и авторизованных пользователей
- 📘 **Интерактивная документация API** через Swagger и Redoc (drf-spectacular)
- ✅ **Набор тестов с отчётом о покрытии** для основных приложений (см. раздел [Тестирование](#-тестирование) ниже)
---
 
## 🛠 Технологический стек
 
| Компонент          | Технология                                |
|----------------------|----------------------------------------------|
| Язык                 | Python 3                                      |
| Фреймворк            | Django 6.1                                    |
| API                  | Django REST Framework                         |
| Авторизация          | Simple JWT (`rest_framework_simplejwt`)       |
| Оплата               | Stripe (Python SDK `stripe`)                  |
| Документация API     | drf-spectacular (Swagger / Redoc)             |
| База данных          | SQLite (для разработки) / готова к PostgreSQL |
| Тестирование         | Django `TestCase` + `coverage.py`             |
| Отладка              | Django Debug Toolbar                          |
| Линтинг              | flake8                                        |
 
---
 
## 📂 Структура проекта
 
```
Library_Service_API/
├── Library_service/     # Настройки проекта, корневые URL
├── books/                # Приложение каталога книг (+ тесты)
├── users/                # Кастомная модель пользователя, регистрация, JWT
├── borrowings/           # Логика выдачи книг: выдать / вернуть (+ тесты)
├── payment/              # Сессии оплаты Stripe, штрафы, статус платежа
├── requirements.txt
├── manage.py
└── .env.example
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
pip install -r requirements.txt
```
 
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
 
# Stripe
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxxx
 
PAYMENT_SUCCESS_URL=http://localhost:3000/payment/success
PAYMENT_CANCEL_URL=http://localhost:3000/payment/cancel
FINE_MULTIPLIER=2
```
 
> 💳 Для локального тестирования оплаты понадобится бесплатный аккаунт [Stripe](https://dashboard.stripe.com/register) и его **тестовые** API-ключи.
 
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
 
| Метод | Эндпоинт                              | Описание                                                                      | Доступ                                  |
|-------|------------------------------------------|------------------------------------------------------------------------------------|-------------------------------------------|
| GET   | `/api/borrowings/`                      | Список выдач (фильтры `?is_active=` / `?user_id=` для персонала)                  | Авторизован (свои записи; персонал — все) |
| GET   | `/api/borrowings/{id}/`                 | Получить одну выдачу                                                                | Авторизован                               |
| POST  | `/api/borrowings/`                      | Выдать книгу — уменьшает запас на 1 и создаёт сессию оплаты Stripe                 | Авторизован                               |
| POST  | `/api/borrowings/{id}/return/`          | Вернуть книгу — увеличивает запас на 1; при просрочке создаёт сессию оплаты **штрафа** | Владелец или персонал                 |
 
### 💳 Платежи (`/api/payments/`)
 
| Метод | Эндпоинт                        | Описание                                                                 | Доступ                          |
|-------|-------------------------------------|-------------------------------------------------------------------------------|-----------------------------------|
| GET   | `/api/payments/`                   | Список платежей (только свои; персонал видит все)                              | Авторизован                       |
| GET   | `/api/payments/{id}/`              | Получить один платёж                                                             | Владелец или персонал             |
| GET   | `/api/payments/success/?session_id=` | Подтвердить сессию оплаты Stripe и пометить платёж как **PAID**              | Публичный (вызывается редиректом Stripe) |
| GET   | `/api/payments/cancel/`            | Уведомление об отмене сессии оплаты                                              | Публичный (вызывается редиректом Stripe) |
 
**Как работает оплата:**
1. При создании выдачи автоматически генерируется **Checkout Session** в Stripe на сумму дневной ставки книги, и к ней привязывается запись `Payment` (`status=PENDING`, `type=PAYMENT`).
2. Пользователь завершает оплату по полученной ссылке `session_url`; Stripe перенаправляет его на `/api/payments/success/` или `/api/payments/cancel/`.
3. Если книга возвращена **позже** `expected_return_date`, автоматически создаётся ещё одна сессия Stripe для начисленного **штрафа** (`type=FINE`), рассчитанного как `daily_fee × дни_просрочки × FINE_MULTIPLIER`.
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
 
| Роль                  | Права доступа                                                                          |
|-------------------------|---------------------------------------------------------------------------------------------|
| **Аноним**             | Просмотр каталога книг, регистрация, получение токена                                      |
| **Авторизованный пользователь** | Управление своим профилем, выдача/возврат книг, просмотр своих выдач и платежей     |
| **Персонал / Админ**  | Полный доступ — управление книгами, просмотр и управление выдачами и платежами всех пользователей |
 
---
 
## ✅ Тестирование
 
В проекте есть набор тестов на базе Django `TestCase`, покрывающий основную бизнес-логику:
 
- **`books/tests.py`** — CRUD книг, фильтрация по названию/автору, проверка прав доступа (персонал vs. пользователи только для чтения)
- **`borrowings/tests.py`** — наиболее полно покрытый модуль: создание выдачи, обновление запасов, действие `return`, расчёт штрафа за просрочку, разграничение доступа (свои выдачи vs. доступ персонала ко всем)
- **`users/tests.py`** и **`payment/tests.py`** — базовые проверки, с возможностью расширения
Запуск полного набора тестов:
 
```bash
python manage.py test
```
 
Запуск тестов с отчётом о покрытии:
 
```bash
coverage run manage.py test
coverage report
```
 
Генерация HTML-отчёта о покрытии (открывается как `htmlcov/index.html`):
 
```bash
coverage html
```
 
> 📈 В репозитории уже есть сгенерированный отчёт `htmlcov/` и конфигурация `.coveragerc`, так что текущее покрытие можно посмотреть без повторного запуска тестов.
 
---
 
## 📄 Лицензия
 
Проект доступен для учебного и личного использования. Добавьте лицензию по своему усмотрению (MIT, Apache 2.0 и т.д.).
 



