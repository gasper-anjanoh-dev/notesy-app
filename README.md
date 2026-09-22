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
- Creates the `/notesy/dev/features/dark-mode-banner` SSM parameter if it does not exist

## Feature Flag Demo

The notes list includes a dark mode banner controlled by the SSM parameter
`/notesy/dev/features/dark-mode-banner`. The application reads the flag with a
60-second cache and fails closed to `false` if SSM is unavailable.

Supported values:

- `false`: show the standard-mode banner for everyone
- `true`: show the dark-mode banner for everyone
- `25%`: show the dark-mode banner to approximately 25% of users by user ID

The ECS task role can read the `/notesy/*` SSM parameters. The CI workflow
creates the default `false` parameter after publishing both the immutable
commit-SHA image and the moving `latest` image tag.

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
