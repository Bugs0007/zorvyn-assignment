# Zorvyn Assignment

Django REST API for user management, financial records, dashboard summaries, and role-based access control.

## Live API

- Base URL: `https://zorvyn-assignment-production-79b6.up.railway.app`
- Postman: import the provided collection and run the `Login` request inside each role folder first

## Implemented Features

- User authentication with bearer token login
- User and role management
- Financial record CRUD
- Record filtering by type, category, and date
- Dashboard summary with totals and category-wise aggregates
- Role-based access control for `ADMIN`, `ANALYST`, and `VIEWER`
- Input validation and error handling
- Persistent deployed database

Note: dashboard trend analytics are not implemented in the current version.

## Roles

- `ADMIN`: full access to users, records, and dashboard
- `ANALYST`: read-only access to records, dashboard access allowed, user management blocked
- `VIEWER`: read-only access to records, dashboard blocked, user management blocked

## Record Validation Rules

- `title` is required and cannot be blank
- `category` is required and cannot be blank
- `amount` must be greater than `0`
- `entry_date` cannot be in the future
- exact duplicate records are rejected

Duplicate policy:

- Exact duplicates are not allowed
- A duplicate means same `title`, `description`, `record_type`, `category`, `amount`, and `entry_date`
- This keeps the financial summary from being inflated by accidental repeated submissions

## Main Endpoints

- `POST /api/users/login/`
- `GET /api/users/me/`
- `GET /api/users/`
- `POST /api/users/`
- `PUT /api/users/{id}/`
- `PATCH /api/users/{id}/`
- `DELETE /api/users/{id}/`
- `GET /api/records/`
- `POST /api/records/`
- `GET /api/records/{id}/`
- `PUT /api/records/{id}/`
- `PATCH /api/records/{id}/`
- `DELETE /api/records/{id}/`
- `GET /api/dashboard/`

## Supported Record Filters

- `record_type`
- `category`
- `category__icontains`
- `entry_date`
- `entry_date__gte`
- `entry_date__lte`

Example:

```text
/api/records/?record_type=INCOME&entry_date__gte=2026-04-01&entry_date__lte=2026-04-30
```

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_finance_data
.\.venv\Scripts\python.exe manage.py runserver
```

## Test Accounts

- `admin / admin123`
- `analyst / analyst123`
- `viewer / viewer123`

## Deployment Notes

- Railway deployment uses `gunicorn`
- SQLite is mounted through a persistent volume
- API authentication uses `Authorization: Bearer <token>`
