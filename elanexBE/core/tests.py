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
