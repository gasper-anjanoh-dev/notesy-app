# Notesy App

A Django notes application containerized with Docker and deployed via CI/CD pipelines.

## Tech Stack

- **Backend:** Django, Gunicorn, PostgreSQL
- **Frontend:** HTMX, TypeScript
- **Container:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Registry:** GitHub Container Registry (GHCR)

## Local Development

```bash
# Clone the repo
git clone https://github.com/gasper-anjanoh-dev/notesy-app.git
cd notesy-app

# Create virtual environment
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
npm install && npm run build

# Run locally
python manage.py migrate
python manage.py seed
python manage.py runserver
```

Visit http://localhost:8000 — login as `demo` / `demo`

## Docker

```bash
# Start full stack (Django + PostgreSQL)
docker compose up --build

# Seed demo data
docker compose exec web python manage.py seed

# Stop
docker compose down
```

## CI/CD Pipeline

On every pull request targeting `main`:
- Runs pytest test suite
- Compiles TypeScript
- Scans dependencies for vulnerabilities

On merge to `main`:
- Builds Docker image
- Pushes to GitHub Container Registry
- Tagged with `:latest` and `:<git-sha>`

## Environment Variables

Copy `.env.example` to `.env` and fill in values:

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| DJANGO_SECRET_KEY | Django secret key |
| DJANGO_DEBUG | True for local, False for production |
| DJANGO_ALLOWED_HOSTS | Comma-separated list of allowed hosts |
| DATABASE_URL | PostgreSQL connection string |

## Security

- No hardcoded secrets — all config via environment variables
- Non-root container user
- Security headers configured (XSS, CSRF, clickjacking protection)
- Database-backed sessions (survives container restarts)
- Dependency vulnerability scanning in CI
