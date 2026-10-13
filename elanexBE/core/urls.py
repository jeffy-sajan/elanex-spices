from django.urls import path

from .views import health_check, products_list


urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("products/", products_list, name="products-list"),
]
