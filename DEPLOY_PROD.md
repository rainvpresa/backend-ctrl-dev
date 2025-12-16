# Production deployment (Docker Compose) — minimal guide

1) Prepare `.env.production`
   - Copy `.env.production.example` to `.env.production` and set real values (SECRET_KEY, DATABASE_URL, etc.).

2) Build and start (on target VM)
   - Install Docker and Docker Compose on the Proxmox guest OS (Ubuntu recommended).
   - From the repository root:

```powershell
docker compose -f docker-compose.prod.yml build --pull
docker compose -f docker-compose.prod.yml up -d
```

3) Run migrations & collectstatic

```powershell
docker compose -f docker-compose.prod.yml run --rm web python manage.py migrate
docker compose -f docker-compose.prod.yml run --rm web python manage.py collectstatic --noinput
```

4) Create superuser (optional)

```powershell
docker compose -f docker-compose.prod.yml run --rm web python manage.py createsuperuser
```

5) Notes
   - The `nginx` container serves `/static/` and `/media/` from the mounted host directories. For TLS/HTTPS, either provision a certificate on the host and mount it into the nginx container, or place an external reverse proxy that terminates TLS in front of this setup (recommended for production).
   - Ensure the Postgres initialization variables are set in `.env.production` so the running Postgres container creates the database you expect. For example:

```
POSTGRES_DB=agham_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=strong-password
DATABASE_URL=postgres://postgres:strong-password@db:5432/agham_db
```

   - When `docker compose` starts the Postgres image for the first time it will create the DB specified by `POSTGRES_DB` and the user/password provided. Make sure these match your `DATABASE_URL`.
   - Consider using a process manager or systemd unit that runs `docker compose -f docker-compose.prod.yml up -d` on reboot.
