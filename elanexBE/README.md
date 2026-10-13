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

## Contact form email delivery

The contact form sends the visitor's name, email address, and message to
`/api/contact/`. Django delivers the message through Resend; the Resend API key
is never exposed to the frontend.

Create a Resend account, verify the sending domain, and add these server-only
values to `.env`:

```text
RESEND_API_KEY=re_...
CONTACT_FROM_EMAIL=website@your-verified-domain.com
CONTACT_RECIPIENT_EMAIL=elanexspices@gmail.com
```

`CONTACT_FROM_EMAIL` must use a verified Resend domain. The visitor's address
is set as the reply-to address so the client can reply directly from the
received email. Do not use the visitor's address as the sender.

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

Product names may repeat. Each product receives a unique internal slug for
frontend links; repeated names receive a numeric suffix such as `8-mm-2`.

Admin operations fail with an actionable message instead of exposing a
traceback. If a database save fails after an image upload, the newly uploaded
image is cleaned up. If old-image cleanup fails after a successful save or
delete, the database operation remains successful and Django records a
warning so the Storage object can be removed later.

## Validation

```powershell
python manage.py check
python manage.py check --deploy
python manage.py collectstatic --noinput
python manage.py test
```

For deployment, set `DJANGO_DEBUG=False`, a strong `DJANGO_SECRET_KEY`,
`DJANGO_ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`, and
`DATABASE_URL` in the hosting provider's secret environment settings. Run
migrations before starting the web process and use a production WSGI/ASGI
server rather than `runserver`.

For Render from the repository root, use:

```text
Build Command: pip install -r elanexBE/requirements.txt && python elanexBE/manage.py collectstatic --noinput && python elanexBE/manage.py migrate
Start Command: cd elanexBE && gunicorn config.wsgi:application
```

Set the backend's environment variables in Render's Environment page. Never
paste `.env` into Git or expose server-only values to the frontend.

The public product catalogue uses a five-minute browser/CDN cache. The frontend
also stores the catalogue locally for five minutes and shares an in-flight
request when multiple pages request products at the same time. Product changes
will therefore normally appear within five minutes without requiring Redis.
