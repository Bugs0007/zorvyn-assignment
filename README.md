# Finance System Backend

Minimal Django REST Framework backend for a finance system with custom users, financial records, dashboard summary APIs, role-based permissions, and token authentication.

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite
- Django Filter

## Setup

1. Create and activate the virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. Run migrations.

```powershell
.\.venv\Scripts\python.exe manage.py makemigrations
.\.venv\Scripts\python.exe manage.py migrate
```

If you already had an older `db.sqlite3`, make sure `migrate` is run again after pulling the latest changes so the DRF token table is created.

4. Seed sample data.

```powershell
.\.venv\Scripts\python.exe manage.py seed_finance_data
```

5. Start the development server.

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

## Authentication

The project uses token authentication with the `Bearer` scheme. The intended reviewer flow is:

1. Call the login API with username and password
2. Copy the returned token
3. Use that token in Postman `Bearer Token` auth or send `Authorization: Bearer <token>`

Login and get a token:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/users/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

If login returns `500 Internal Server Error` with `no such table: authtoken_token`, run:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

Use the returned token in later requests:

```powershell
curl.exe http://127.0.0.1:8000/api/users/me/ ^
  -H "Authorization: Bearer <your_token>"
```

## API Endpoints

The following endpoints are mounted by the current project URL configuration:

- `POST /api/users/login/` - login and get auth token
- `GET /api/users/` - list users
- `POST /api/users/` - create user
- `GET /api/users/{id}/` - retrieve user
- `PUT /api/users/{id}/` - update user
- `PATCH /api/users/{id}/` - partial update user
- `DELETE /api/users/{id}/` - delete user
- `GET /api/users/me/` - current authenticated user
- `GET /api/records/` - list records
- `POST /api/records/` - create record
- `GET /api/records/{id}/` - retrieve record
- `PUT /api/records/{id}/` - update record
- `PATCH /api/records/{id}/` - partial update record
- `DELETE /api/records/{id}/` - delete record
- `GET /api/dashboard/` - dashboard summary

## Reviewer Testing Guide

Base URL:

```text
http://127.0.0.1:8000
```

Start the server:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

### Sample Users

Created by `seed_finance_data` and used for login testing:

- `admin / admin123`
- `analyst / analyst123`
- `viewer / viewer123`

### Roles and Permissions

- `ADMIN` - full access to users, records, and dashboard
- `ANALYST` - read-only access to users and records, access to dashboard
- `VIEWER` - read-only access to users and records, no dashboard access

### User APIs

Login and get token:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/users/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

Get current user with token auth:

```powershell
curl.exe http://127.0.0.1:8000/api/users/me/ ^
  -H "Authorization: Bearer <your_token>"
```

List users as admin:

```powershell
curl.exe http://127.0.0.1:8000/api/users/ ^
  -H "Authorization: Bearer <admin_token>"
```

Create a user as admin:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/users/ ^
  -H "Authorization: Bearer <admin_token>" ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"demo_user\",\"password\":\"demo12345\",\"email\":\"demo@example.com\",\"role\":\"VIEWER\"}"
```

Verify the created user can log in:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/users/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"demo_user\",\"password\":\"demo12345\"}"
```

Retrieve a user by id:

```powershell
curl.exe http://127.0.0.1:8000/api/users/1/ ^
  -H "Authorization: Bearer <admin_token>"
```

Update a user:

```powershell
curl.exe -X PUT http://127.0.0.1:8000/api/users/1/ ^
  -H "Authorization: Bearer <admin_token>" ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"admin\",\"email\":\"admin@example.com\",\"first_name\":\"Admin\",\"last_name\":\"User\",\"role\":\"ADMIN\",\"is_active\":true}"
```

Partially update a user:

```powershell
curl.exe -X PATCH http://127.0.0.1:8000/api/users/1/ ^
  -H "Authorization: Bearer <admin_token>" ^
  -H "Content-Type: application/json" ^
  -d "{\"first_name\":\"Finance\"}"
```

Change a user's password:

```powershell
curl.exe -X PATCH http://127.0.0.1:8000/api/users/4/ ^
  -H "Authorization: Bearer <admin_token>" ^
  -H "Content-Type: application/json" ^
  -d "{\"password\":\"newpass123\"}"
```

Verify login with the updated password:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/users/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"demo_user\",\"password\":\"newpass123\"}"
```

Delete a user:

```powershell
curl.exe -X DELETE http://127.0.0.1:8000/api/users/4/ ^
  -H "Authorization: Bearer <admin_token>"
```

Expected permission check as viewer:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/users/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"viewer\",\"password\":\"viewer123\"}"
```

Then use the returned viewer token:

```powershell
curl.exe -i http://127.0.0.1:8000/api/users/ ^
  -H "Authorization: Bearer <viewer_token>"
```

### Record APIs

List records:

```powershell
curl.exe http://127.0.0.1:8000/api/records/ ^
  -H "Authorization: Bearer <admin_token>"
```

Create a record as admin:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/records/ ^
  -H "Authorization: Bearer <admin_token>" ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"April Salary\",\"description\":\"Monthly salary credited\",\"record_type\":\"INCOME\",\"category\":\"Salary\",\"amount\":\"50000.00\",\"entry_date\":\"2026-04-01\"}"
```

Retrieve a record by id:

```powershell
curl.exe http://127.0.0.1:8000/api/records/1/ ^
  -H "Authorization: Bearer <admin_token>"
```

Update a record:

```powershell
curl.exe -X PUT http://127.0.0.1:8000/api/records/1/ ^
  -H "Authorization: Bearer <admin_token>" ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"April Salary Updated\",\"description\":\"Revised amount\",\"record_type\":\"INCOME\",\"category\":\"Salary\",\"amount\":\"52000.00\",\"entry_date\":\"2026-04-01\"}"
```

Partially update a record:

```powershell
curl.exe -X PATCH http://127.0.0.1:8000/api/records/1/ ^
  -H "Authorization: Bearer <admin_token>" ^
  -H "Content-Type: application/json" ^
  -d "{\"category\":\"Primary Salary\"}"
```

Delete a record:

```powershell
curl.exe -X DELETE http://127.0.0.1:8000/api/records/1/ ^
  -H "Authorization: Bearer <admin_token>"
```

Expected permission check as analyst on create:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/users/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"analyst\",\"password\":\"analyst123\"}"
```

Then use the returned analyst token:

```powershell
curl.exe -i -X POST http://127.0.0.1:8000/api/records/ ^
  -H "Authorization: Bearer <analyst_token>" ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Test\",\"description\":\"Should fail\",\"record_type\":\"EXPENSE\",\"category\":\"Food\",\"amount\":\"250.00\",\"entry_date\":\"2026-04-05\"}"
```

### Record Filters

`/api/records/` supports:

- `record_type`
- `category`
- `category__icontains`
- `entry_date`
- `entry_date__gte`
- `entry_date__lte`

Filter by record type:

```powershell
curl.exe "http://127.0.0.1:8000/api/records/?record_type=INCOME" ^
  -H "Authorization: Bearer <admin_token>"
```

Filter by category search:

```powershell
curl.exe "http://127.0.0.1:8000/api/records/?category__icontains=sal" ^
  -H "Authorization: Bearer <admin_token>"
```

Filter by date range:

```powershell
curl.exe "http://127.0.0.1:8000/api/records/?entry_date__gte=2026-04-01&entry_date__lte=2026-04-30" ^
  -H "Authorization: Bearer <admin_token>"
```

### Dashboard API

Dashboard as admin:

```powershell
curl.exe http://127.0.0.1:8000/api/dashboard/ ^
  -H "Authorization: Bearer <admin_token>"
```

Dashboard as analyst:

```powershell
curl.exe http://127.0.0.1:8000/api/dashboard/ ^
  -H "Authorization: Bearer <analyst_token>"
```

Expected permission check as viewer:

```powershell
curl.exe -i http://127.0.0.1:8000/api/dashboard/ ^
  -H "Authorization: Bearer <viewer_token>"
```

## Dashboard Response

The dashboard API returns:

- total income
- total expense
- net balance
- category-wise totals

## Assumptions

- SQLite is used for local development only.
- Authentication is handled with DRF token authentication using the `Bearer` scheme.
- Role-based access is enforced at the API layer.
- The dashboard is read-only and uses ORM aggregation over stored records.
- This project is backend-only and does not include a frontend client.
