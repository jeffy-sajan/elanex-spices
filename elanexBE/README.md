# Elanex backend

The backend is a Django REST API. It currently provides the foundation for the
cardamom marketing site and is structured so product, content, and ecommerce
features can be added without changing the frontend contract.

## Local setup

From `elanexBE`:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```

The health endpoint is available at
`http://127.0.0.1:8000/api/health/`.

## Configuration

The default local database is SQLite. Set `DATABASE_URL` to the Supabase
PostgreSQL connection string in deployment environments. Never commit `.env`
or database credentials.

`CORS_ALLOWED_ORIGINS` accepts a comma-separated list and defaults to the
local Next.js development origin.

## Validation

```powershell
python manage.py check
python manage.py test
```
