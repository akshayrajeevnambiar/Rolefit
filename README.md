# RoleFit

RoleFit will compare job descriptions with a résumé and show skill gaps. This repository has the Django API, a React frontend, Postgres, and CI. You can register, sign in, and save a résumé or a job description. Nothing reads those texts for skills yet.

## Stack

- Python 3.12, Django 5.2, Django REST Framework
- PostgreSQL 16 (`pgvector/pgvector`, extension enabled on first boot)
- React, TypeScript, Vite
- Docker Compose for local running
- GitHub Actions for lint, tests, gitleaks, and dependency scans

## Run locally

Install Docker with Compose v2. From the repository root:

```bash
cp .env.example .env
docker compose up --build
```

That file is how you turn debug on for this laptop. Compose leaves `DJANGO_DEBUG` off when it is unset, and it publishes Postgres, the API, and Vite on `127.0.0.1` only. Do not put real secrets in either file.

Then open:

- Frontend: http://localhost:5173
- API health check: http://localhost:8000/api/health/

The health check returns `{"status": "ok"}`. It does not query the database. On startup the API container runs `manage.py migrate`, which creates the account, résumé, job description, and analysis tables in Postgres.

Stop the stack with `docker compose down`. Add `-v` to delete the database volume.

The Compose files start Django's development server and the Vite dev server. Production hosting is a later pull request.

## Run checks without Docker

Backend:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements-dev.txt
cd backend
ruff check . && ruff format --check .
DJANGO_DEBUG=true python manage.py check
DJANGO_DEBUG=true pytest
```

`pytest` does not need Postgres. It uses `config/test_settings.py`, which points Django at SQLite in memory. `DJANGO_DEBUG=true` is required when `.env` is absent: with debug off, Django refuses the public dev secret and any secret shorter than 50 characters. Copying `.env.example` sets the debug flag.

Frontend (Node.js 22):

```bash
cd frontend
npm ci
npm run lint
npm run format:check
npm test
npm run build
```

Pre-commit runs the same lint tools plus gitleaks before each commit:

```bash
pip install pre-commit
pre-commit install
```

The frontend hooks need `npm ci` inside `frontend/` first.

## Design tokens

The placeholder page imports `design/tokens.css`. That file is the Proof palette and type: warm gray (`#f7f6f3`), Schibsted Grotesk for the interface, and IBM Plex Mono for the short “Local only” line. The font files are in `design/fonts/` and are loaded from `frontend/src/styles.css`.

In the frontend image the app lives at `/app`, so the import `../../design/tokens.css` is the path `/design/tokens.css`. Compose mounts `design/` there, read-only.

## API

The browser talks to Vite, and Vite forwards `/api` to Django. Cookies stay on that one origin. There is no cross-origin setup.

`GET /api/health/` is public. Every other route requires a signed-in account unless it opts out. HTTP Basic authentication is not enabled.

| Method | Path | Who |
|---|---|---|
| GET | `/api/auth/csrf/` | Anyone. Sets the CSRF cookie. |
| POST | `/api/auth/register/` | Anyone with that cookie. Creates the account and signs them in. |
| POST | `/api/auth/login/` | Anyone with that cookie. |
| POST | `/api/auth/logout/` | The signed-in account. |
| GET | `/api/auth/me/` | The signed-in account. |
| GET, POST | `/api/resumes/` | The signed-in account, only their rows. |
| GET, PUT, PATCH, DELETE | `/api/resumes/<id>/` | The owner. Anyone else gets 404. |
| GET, POST | `/api/job-descriptions/` | The signed-in account, only their rows. |
| GET, PUT, PATCH, DELETE | `/api/job-descriptions/<id>/` | The owner. Anyone else gets 404. |

Register and login take `{"email", "password"}` as JSON. Send the CSRF cookie back as the `X-CSRFToken` header on every call after the cookie exists, including `GET /api/auth/me/`. Login and logout replace the cookie, so the next call uses the new value. Register and login share a limit of 5 attempts a minute from the connection address. A client-supplied `X-Forwarded-For` does not get its own limit.

An analysis row can link one résumé to one job description for that same account. There is no URL for it, and nothing fills it in.

## What is not here yet

Skill extraction, gap results, and deployment. The screen is still the placeholder.
