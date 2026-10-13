from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_active", "display_order")
    list_filter = ("category", "is_active")
    list_editable = ("price", "is_active", "display_order")
    search_fields = ("name", "slug", "description", "grade")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("display_order", "name")
