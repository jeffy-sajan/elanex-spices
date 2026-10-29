from django.core.management.base import BaseCommand

from core.catalog import write_product_catalog
from core.models import Product


class Command(BaseCommand):
    help = "Export the database product catalogue to the public JSON cache."

    def handle(self, *args, **options):
        payload = write_product_catalog(
            Product.objects.order_by("created_at", "id")
        )
        if payload is None:
            self.stderr.write(
                self.style.ERROR("Product catalogue export is disabled or failed.")
            )
            return
        self.stdout.write(
            self.style.SUCCESS(
                f"Exported {len(payload)} product(s) to the public catalogue cache."
            )
        )
