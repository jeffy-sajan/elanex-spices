import json
import tempfile
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.contrib import admin
from django.db import DatabaseError, IntegrityError
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework.throttling import ScopedRateThrottle
from pathlib import Path

from .admin import ProductAdminForm
from .models import Product

@override_settings(USE_PRODUCT_CATALOG_FILE=False)
class HealthCheckTests(SimpleTestCase):
    def test_health_check_returns_service_status(self):
        response = APIClient().get("/api/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {"status": "ok", "service": "elanex-api"},
        )

    @patch("core.views.Product.objects.all", side_effect=DatabaseError("database unavailable"))
    def test_catalogue_database_failure_returns_safe_error(self, products):
        response = APIClient().get("/api/products/")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.data,
            {"detail": "The product catalogue is temporarily unavailable."},
        )


class ContactMessageTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._old_throttle_rates = ScopedRateThrottle.THROTTLE_RATES
        ScopedRateThrottle.THROTTLE_RATES = {"contact": "100/minute"}

    @classmethod
    def tearDownClass(cls):
        ScopedRateThrottle.THROTTLE_RATES = cls._old_throttle_rates
        super().tearDownClass()
    @patch("core.views.urllib_request.urlopen")
    @patch("core.views.settings.CONTACT_FROM_EMAIL", "website@example.com")
    @patch("core.views.settings.RESEND_API_KEY", "re_test")
    def test_contact_message_sends_email(self, urlopen):
        urlopen.return_value.__enter__.return_value.status = 200
        response = APIClient().post(
            "/api/contact/",
            {
                "name": "A Buyer",
                "email": "buyer@example.com",
                "message": "Please share your available grades.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        urlopen.assert_called_once()

    def test_contact_message_validates_required_fields(self):
        response = APIClient().post(
            "/api/contact/",
            {"name": "", "email": "invalid", "message": ""},
            format="json",
        )

        self.assertEqual(response.status_code, 400)


@override_settings(USE_PRODUCT_CATALOG_FILE=False)
class ProductApiTests(TestCase):
    def test_products_are_returned_oldest_first(self):
        first = Product.objects.create(
            name="First Product",
            price="100.00",
            image_url="https://example.com/first.png",
        )
        second = Product.objects.create(
            name="Second Product",
            price="200.00",
            image_url="https://example.com/second.png",
        )

        response = APIClient().get("/api/products/")

        self.assertEqual(
            [product["id"] for product in response.data],
            [first.slug, second.slug],
        )
        self.assertEqual(
            response["Cache-Control"],
            "public, max-age=300, stale-while-revalidate=60",
        )

    def test_products_include_category(self):
        Product.objects.create(
            name="Visible Cardamom",
            slug="visible-cardamom",
            description="A public product.",
            price="1200.00",
            image_url="https://example.com/cardamom.png",
            category=Product.Category.CARDAMOM,
        )
        Product.objects.create(
            name="Aromatic Seeds",
            slug="aromatic-seeds",
            description=None,
            price="800.00",
            image_url="https://example.com/seeds.png",
            category=Product.Category.SEEDS,
        )

        response = APIClient().get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        products_by_id = {product["id"]: product for product in response.data}
        self.assertEqual(products_by_id["visible-cardamom"]["category"], "cardamom")
        self.assertEqual(products_by_id["aromatic-seeds"]["category"], "seeds")
        self.assertEqual(
            set(products_by_id["visible-cardamom"]),
            {"id", "name", "description", "price", "image", "category"},
        )


class ProductCatalogCacheTests(SimpleTestCase):
    def test_api_serves_generated_catalog_without_database_query(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            catalog_directory = Path(temporary_directory) / "data"
            catalog_directory.mkdir()
            (catalog_directory / "products.json").write_text(
                json.dumps(
                    [
                        {
                            "id": "cached-cardamom",
                            "name": "Cached Cardamom",
                            "description": "Cached product",
                            "price": "1200.00",
                            "image": "https://example.com/cached.png",
                            "category": "cardamom",
                        }
                    ]
                ),
                encoding="utf-8",
            )
            with override_settings(
                BASE_DIR=Path(temporary_directory),
                USE_PRODUCT_CATALOG_FILE=True,
            ):
                with patch(
                    "core.views.Product.objects.all",
                    side_effect=AssertionError("database should not be queried"),
                ):
                    response = APIClient().get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["id"], "cached-cardamom")


class ProductAdminTests(TestCase):
    def test_duplicate_names_receive_unique_slugs(self):
        first = Product.objects.create(
            name="8 mm",
            slug="8-mm",
            price="1200.00",
            image_url="https://example.com/existing.png",
        )
        second = Product.objects.create(
            name="8 mm",
            price="1300.00",
            image_url="https://example.com/second.png",
        )

        self.assertEqual(first.slug, "8-mm")
        self.assertEqual(second.slug, "8-mm-2")

    @patch("core.admin.storage_is_configured", return_value=True)
    def test_duplicate_names_are_valid_in_admin_form(self, storage_configured):
        form = ProductAdminForm(
            data={
                "name": "8 mm",
                "description": "",
                "price": "1300",
                "category": Product.Category.CARDAMOM,
            },
            files={
                "image_upload": SimpleUploadedFile(
                    "cardamom.png",
                    b"image",
                    content_type="image/png",
                )
            },
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_price_must_be_positive(self):
        product = Product(
            name="Invalid price",
            price="0.00",
            image_url="https://example.com/image.png",
        )

        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_admin_form_exposes_only_requested_product_fields(self):
        self.assertEqual(
            set(ProductAdminForm().fields),
            {"name", "description", "price", "category", "image_upload"},
        )

    @patch("core.admin.storage_is_configured", return_value=False)
    def test_image_upload_requires_storage_configuration(self, storage_configured):
        form = ProductAdminForm(
            data={
                "name": "Cardamom",
                "description": "",
                "price": "1200",
                "category": Product.Category.CARDAMOM,
            },
            files={
                "image_upload": SimpleUploadedFile(
                    "cardamom.png",
                    b"image",
                    content_type="image/png",
                )
            },
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Supabase Storage is not configured", str(form.errors))

    @patch("core.admin.delete_product_image")
    @patch("core.admin.upload_product_image", return_value=("products/new.png", "https://example.com/new.png"))
    def test_failed_database_save_removes_newly_uploaded_image(
        self,
        upload_image,
        delete_image,
    ):
        existing = Product.objects.create(
            name="Existing",
            slug="existing",
            price="100.00",
            image_url="https://example.com/existing.png",
        )
        duplicate = Product(
            name="Duplicate",
            slug=existing.slug,
            price="200.00",
            image_url="",
        )
        form = SimpleNamespace(cleaned_data={"image_upload": Mock()})
        product_admin = admin.site._registry[Product]

        with self.assertRaises(IntegrityError):
            product_admin.save_model(SimpleNamespace(), duplicate, form, False)

        upload_image.assert_called_once()
        delete_image.assert_called_once_with("products/new.png")
