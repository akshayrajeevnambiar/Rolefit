# RoleFit

RoleFit will compare job descriptions with a résumé and show skill gaps. This repository is the scaffold only: a Django API, a React frontend, Postgres, and CI. There is no product behavior yet.

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

The health check returns `{"status": "ok"}`. It does not query the database. On startup the API container runs `manage.py migrate`, which creates Django's built-in tables in Postgres. This scaffold has no models of its own yet.

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

`pytest` does not need Postgres. The health test never opens a database connection. `DJANGO_DEBUG=true` is required when `.env` is absent: with debug off, Django refuses the public dev secret. Copying `.env.example` sets the same flag.

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

## What is not here yet

Models, sign-in, job-description APIs, the extraction pipeline, and deployment. `GET /api/health/` is public. Any new API route requires an authenticated user unless it opts out, and HTTP Basic authentication is not enabled.
