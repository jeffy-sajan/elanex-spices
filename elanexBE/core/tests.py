from django.test import SimpleTestCase, TestCase
from rest_framework.test import APIClient

from .models import Product

class HealthCheckTests(SimpleTestCase):
    def test_health_check_returns_service_status(self):
        response = APIClient().get("/api/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {"status": "ok", "service": "elanex-api"},
        )


class ProductApiTests(TestCase):
    def test_only_active_products_are_public(self):
        Product.objects.create(
            name="Visible Cardamom",
            slug="visible-cardamom",
            description="A public product.",
            price="1200.00",
            image_url="https://example.com/cardamom.png",
            grade="Premium",
        )
        Product.objects.create(
            name="Hidden Cardamom",
            slug="hidden-cardamom",
            description="An inactive product.",
            price="1000.00",
            image_url="https://example.com/hidden.png",
            grade="Standard",
            is_active=False,
        )

        response = APIClient().get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], "visible-cardamom")
