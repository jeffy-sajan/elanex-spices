import json
import logging
from pathlib import Path

from django.conf import settings

logger = logging.getLogger(__name__)


def product_catalog_path():
    base_dir = Path(getattr(settings, "BASE_DIR", Path(__file__).resolve().parent.parent))
    return base_dir / "data" / "products.json"


def product_catalog_enabled():
    return str(getattr(settings, "USE_PRODUCT_CATALOG_FILE", True)).lower() not in {
        "false",
        "0",
        "no",
    }


def serialize_products(product_queryset):
    product_data = []
    for product in product_queryset:
        product_data.append(
            {
                "id": product.slug,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "image": product.image_url,
                "category": product.category,
            }
        )
    return product_data


def write_product_catalog(product_queryset):
    if not product_catalog_enabled():
        return None

    catalog_path = product_catalog_path()
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    payload = serialize_products(product_queryset)

    temporary_path = catalog_path.with_suffix(".json.tmp")
    try:
        temporary_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary_path.replace(catalog_path)
    except OSError:
        logger.exception("Could not persist the product catalog JSON file.")
        try:
            temporary_path.unlink(missing_ok=True)
        except OSError:
            logger.exception("Could not remove the temporary product catalog file.")
        return None

    return payload


def read_product_catalog():
    if not product_catalog_enabled():
        return None

    catalog_path = product_catalog_path()
    if not catalog_path.exists():
        return None

    try:
        with catalog_path.open("r", encoding="utf-8") as file_handle:
            payload = json.load(file_handle)
    except (OSError, ValueError):
        logger.warning("Product catalog JSON could not be read; falling back to database.")
        return None

    if isinstance(payload, list):
        return payload
    return None
