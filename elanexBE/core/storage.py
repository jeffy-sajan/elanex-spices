import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
MAX_IMAGE_SIZE = 5 * 1024 * 1024


def _ensure_storage_config() -> None:
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
        raise ImproperlyConfigured(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required for image uploads."
        )


def _storage_url(path: str) -> str:
    _ensure_storage_config()
    return (
        f"{settings.SUPABASE_URL}/storage/v1/object/"
        f"{settings.SUPABASE_STORAGE_BUCKET}/{path}"
    )


def upload_product_image(uploaded_file) -> tuple[str, str]:
    content_type = uploaded_file.content_type or ""
    extension = ALLOWED_IMAGE_TYPES.get(content_type)
    if extension is None:
        raise ValueError("Upload a JPEG, PNG, or WebP image.")
    if uploaded_file.size > MAX_IMAGE_SIZE:
        raise ValueError("Product images must be 5 MB or smaller.")

    path = f"products/{uuid4().hex}{extension}"
    request = Request(
        _storage_url(path),
        data=uploaded_file.read(),
        method="POST",
        headers={
            "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
            "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
            "Content-Type": content_type,
            "x-upsert": "false",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            if response.status not in (200, 201):
                raise RuntimeError(
                    f"Supabase Storage upload failed with status {response.status}."
                )
    except (HTTPError, URLError) as error:
        raise RuntimeError("Supabase Storage image upload failed.") from error

    public_url = (
        f"{settings.SUPABASE_URL}/storage/v1/object/public/"
        f"{settings.SUPABASE_STORAGE_BUCKET}/{path}"
    )
    return path, public_url


def delete_product_image(path: str) -> None:
    if not path:
        return
    _ensure_storage_config()
    request = Request(
        f"{settings.SUPABASE_URL}/storage/v1/object/remove/"
        f"{settings.SUPABASE_STORAGE_BUCKET}",
        data=json.dumps({"prefixes": [path]}).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
            "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            if response.status not in (200, 204):
                raise RuntimeError(
                    f"Supabase Storage deletion failed with status {response.status}."
                )
    except (HTTPError, URLError) as error:
        raise RuntimeError("Supabase Storage image deletion failed.") from error
