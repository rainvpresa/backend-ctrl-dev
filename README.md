# AGHAMazingQuest — Backend

This repository contains the Django API for AGHAMazingQuest and Docker compose files for development and production.

Summary
- Backend: Django + Django REST Framework
- Auth: JWT via SimpleJWT, dj-rest-auth and django-allauth (OTP email login implemented)
- DB: PostgreSQL
- Frontend: web CMS in `frontend/cms/`; mobile client is a Unity project (not included here)

Quickstart — Development
1. Copy and edit env file:
```powershell
copy .env.example .env
notepad .env
```
2. Build and start the development stack (uses `docker-compose.yml`):
```powershell
docker compose up --build
```
3. Run migrations and create a superuser:
```powershell
docker compose exec api python manage.py migrate
docker compose exec api python manage.py createsuperuser
```

Quickstart — Production (VM)
- Use `docker-compose.prod.yml` and `.env.production` (create from `.env.production.example`).
- Example commands:
```powershell
docker compose -f docker-compose.prod.yml build --pull
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml run --rm web python manage.py migrate
docker compose -f docker-compose.prod.yml run --rm web python manage.py collectstatic --noinput
```

Important notes
- Profile fields (`display_name`, `avatar`) live on `accounts.User` (the `profiles` app was removed).
- Media uploads are saved to `MEDIA_ROOT` (`/media/` URL). Ensure `Pillow` is installed.
- OTP endpoints:
  - `POST /api/auth/otp/request/` — request login code
  - `POST /api/auth/otp/verify/` — verify code and receive JWT tokens
- Standard auth endpoints are exposed under `/api/auth/` via `dj-rest-auth` and `allauth` (login, logout, registration, social).

If you need any of the following, tell me and I will add them:
- A short Postman/HTTPie collection to exercise the OTP + JWT flow
- A data migration script to copy legacy `profiles` rows into `accounts.User` before you run migrations
- TLS automation for the production compose (Let's Encrypt)

Minimal support contact
- For repo changes or deploy artifacts I added: `docker-compose.prod.yml`, `deploy/nginx/default.conf`, and `.env.production.example`.

