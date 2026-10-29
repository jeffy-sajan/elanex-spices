import json
import logging
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


logger = logging.getLogger(__name__)

ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
MAX_IMAGE_SIZE = 5 * 1024 * 1024


class StorageOperationError(RuntimeError):
    """Raised when Supabase Storage cannot complete an image operation."""


def storage_is_configured() -> bool:
    return bool(settings.SUPABASE_URL and settings.SUPABASE_SERVICE_ROLE_KEY)


def _ensure_storage_config() -> None:
    if not storage_is_configured():
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
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:300]
        raise StorageOperationError(
            f"Supabase Storage image upload failed (HTTP {error.code}): {detail}"
        ) from error
    except URLError as error:
        raise StorageOperationError(
            f"Supabase Storage image upload failed: {error.reason}"
        ) from error

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
                raise StorageOperationError(
                    f"Supabase Storage deletion failed with status {response.status}."
                )
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:300]
        if error.code == 404 or "NoSuchBucket" in detail or '"statusCode":"404"' in detail:
            logger.warning(
                "Supabase image cleanup skipped because the storage object or "
                "bucket no longer exists: %s",
                path,
            )
            return
        raise StorageOperationError(
            f"Supabase Storage image deletion failed (HTTP {error.code}): {detail}"
        ) from error
    except URLError as error:
        raise StorageOperationError(
            f"Supabase Storage image deletion failed: {error.reason}"
        ) from error
