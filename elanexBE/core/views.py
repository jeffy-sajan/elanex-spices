from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from .models import Product

class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response(
            {"status": "ok", "service": "elanex-api"},
            status=HTTP_200_OK,
        )


health_check = HealthCheckView.as_view()


class ProductListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        products = Product.objects.filter(is_active=True)
        return Response(
            [
                {
                    "id": product.slug,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "image": product.image_url,
                    "category": product.category,
                    "badge": product.badge or None,
                    "grade": product.grade,
                }
                for product in products
            ],
            status=HTTP_200_OK,
        )


products_list = ProductListView.as_view()
