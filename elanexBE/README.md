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

The public product catalog is available at
`http://127.0.0.1:8000/api/products/`. Products are managed through the Django
admin at `http://127.0.0.1:8000/admin/`.

## Configuration

Set `DJANGO_DEBUG=True` for local development; SQLite is available only in
development mode. Set `DJANGO_DEBUG=False` in deployment environments, where
both `DJANGO_SECRET_KEY` and `DATABASE_URL` are required. `DATABASE_URL` must
contain the Supabase PostgreSQL connection string. Never commit `.env` or
database credentials.

`CORS_ALLOWED_ORIGINS` accepts a comma-separated list and defaults to the
local frontend development origins.

## Product administration

Create an admin account once from `elanexBE`:

```powershell
python manage.py createsuperuser
```

Before uploading product images, create a public Supabase Storage bucket named
`product-images` (or set `SUPABASE_STORAGE_BUCKET` to another bucket name).
Set `SUPABASE_URL` and the server-only `SUPABASE_SERVICE_ROLE_KEY` in `.env`.
Never expose the service-role key to the frontend.

After starting the server, sign in at `/admin/` and add products under
**Core > Products**. The admin form accepts the product name, category
(**Cardamom** or **Seeds**), description (optional), price in INR, and a JPEG,
PNG, or WebP image. The image file is stored in Supabase Storage and its
public URL and Storage path
are saved with the product row in Supabase PostgreSQL. Replacing an image
removes the previous Storage object; deleting a product removes both the
database row and its Storage object.

Admin operations fail with an actionable message instead of exposing a
traceback. If a database save fails after an image upload, the newly uploaded
image is cleaned up. If old-image cleanup fails after a successful save or
delete, the database operation remains successful and Django records a
warning so the Storage object can be removed later.

## Validation

```powershell
python manage.py check
python manage.py test
```
