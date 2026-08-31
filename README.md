# Nanded District Taluka Management System — Backend

Django REST Framework API for Nanded district taluka administration.

This repository is **backend only**. There is no Flutter, React, or HTML frontend.

**DEMO CREDENTIALS ARE FOR DEVELOPMENT ONLY. Change every demo password before production.**

## Installation (Windows)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_nanded
python manage.py runserver
```

## Installation (macOS / Linux)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_nanded
python manage.py runserver
```

## URLs

| Resource | URL |
| --- | --- |
| API | http://127.0.0.1:8000/api/ |
| Swagger / OpenAPI UI | http://127.0.0.1:8000/api/docs/ |
| OpenAPI schema | http://127.0.0.1:8000/api/schema/ |
| Django Admin | http://127.0.0.1:8000/admin/ |

Login to Django Admin as `admin` / `Admin@12345` (demo only).

## Demo login

See [DEMO_ACCOUNTS.md](DEMO_ACCOUNTS.md) for the full matrix.

| Username | Password | Role | Scope |
| --- | --- | --- | --- |
| `admin` | `Admin@12345` | SUPER_ADMIN | All talukas |
| `hadgaon.tahsildar` | `Tahsildar@123` | TAHSILDAR | Hadgaon only |
| `hadgaon.user1` | `User@12345` | TALUKA_USER | Hadgaon only |

All 16 tahsildars use password `Tahsildar@123`.  
All taluka users use password `User@12345`.

## Roles

- **SUPER_ADMIN** — district-wide users, tahsildars, records, dashboards, audit logs, password resets, moving users between talukas. `taluka` is always `null`.
- **TAHSILDAR** — one taluka. Can manage that taluka's `TALUKA_USER` accounts and records. Cannot create tahsildars, cannot change own taluka, cannot promote themselves.
- **TALUKA_USER** — one taluka. Can view/create records in their taluka. Cannot manage users, change role/taluka, or call admin APIs.

**Taluka isolation is enforced in Django querysets, serializers, and permissions.** A client cannot access another taluka by changing IDs in the request.

## One primary Tahsildar per taluka

An active `TAHSILDAR` is unique per taluka (database partial unique constraint + API validation).

## Seed command

```bash
python manage.py seed_nanded
```

Idempotent `get_or_create` seeding:

- 1 Super Admin
- 16 Talukas
- 16 Tahsildars
- 48 Taluka Users
- 80 Records (`ARD-001` … `UMR-005`)

## API endpoints

### Auth

| Method | Path |
| --- | --- |
| POST | `/api/auth/login/` |
| POST | `/api/auth/refresh/` |
| POST | `/api/auth/logout/` |
| GET | `/api/auth/me/` |
| POST | `/api/auth/change-password/` |

Login body: `{"username": "admin", "password": "Admin@12345"}`.  
Use `Authorization: Bearer <access>`.

### Dashboards

| Method | Path | Who |
| --- | --- | --- |
| GET | `/api/dashboard/admin/` | SUPER_ADMIN |
| GET | `/api/dashboard/taluka/` | TAHSILDAR / TALUKA_USER (own taluka only) |

### Talukas

| Method | Path |
| --- | --- |
| GET | `/api/talukas/` |
| GET | `/api/talukas/{id}/` |

### Users

| Method | Path |
| --- | --- |
| GET/POST | `/api/users/` |
| GET/PUT/PATCH/DELETE | `/api/users/{id}/` |
| POST | `/api/users/{id}/activate/` |
| POST | `/api/users/{id}/deactivate/` |
| POST | `/api/users/{id}/reset-password/` |

DELETE is a **soft delete** (`is_active=false`). Password reset is SUPER_ADMIN only.

When a Tahsildar creates a user, the backend sets `role=TALUKA_USER` and `taluka` to the Tahsildar's taluka. A foreign `taluka_id` is rejected.

### Tahsildars (SUPER_ADMIN only)

| Method | Path |
| --- | --- |
| GET/POST | `/api/tahsildars/` |
| GET/PUT/PATCH/DELETE | `/api/tahsildars/{id}/` |

### Records

| Method | Path |
| --- | --- |
| GET/POST | `/api/records/` |
| GET/PUT/PATCH/DELETE | `/api/records/{id}/` |
| POST | `/api/records/{id}/activate/` |
| POST | `/api/records/{id}/deactivate/` |

`taluka` and `record_number` are assigned by the server. DELETE deactivates the record.

### Audit logs (SUPER_ADMIN only)

| Method | Path |
| --- | --- |
| GET | `/api/audit-logs/` |
| GET | `/api/audit-logs/{id}/` |

## Example requests

```http
POST /api/auth/login/
{"username": "hadgaon.tahsildar", "password": "Tahsildar@123"}
```

```http
GET /api/records/
Authorization: Bearer <token>
```

Hadgaon Tahsildar only receives `HAD-001` … records. Requesting a Nanded record ID returns **404**.

```http
POST /api/users/
{"username": "newuser", "first_name": "New", "last_name": "User", "phone": "9999999999", "password": "User@12345"}
```

Tahsildar response includes `role: TALUKA_USER` and Hadgaon `taluka`.

## Tests

```bash
python manage.py test
```

## Environment

Copy `.env.example` to `.env`. Do not commit production secrets.

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Django secret |
| `DEBUG` | `True` / `False` |
| `ALLOWED_HOSTS` | Comma-separated hosts |
| `DATABASE_URL` | Default SQLite; use Postgres in production |
| `CORS_ALLOWED_ORIGINS` | Allowed browser/mobile origins (no production wildcard) |
| `CORS_ALLOW_ALL_ORIGINS` | `False` in production |

## Project structure

```text
nanded-taluka-backend/
├── manage.py
├── config/
├── accounts/
├── talukas/
├── records/
├── audit/
├── requirements.txt
├── .env.example
└── README.md
```
