from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Product
from .storage import (
    ALLOWED_IMAGE_TYPES,
    MAX_IMAGE_SIZE,
    delete_product_image,
    upload_product_image,
)


class ProductAdminForm(forms.ModelForm):
    image_upload = forms.FileField(
        required=False,
        help_text="JPEG, PNG, or WebP, maximum 5 MB.",
    )

    class Meta:
        model = Product
        exclude = ("slug", "image_url", "image_path")

    def clean_image_upload(self):
        image = self.cleaned_data.get("image_upload")
        if image is None and not self.instance.pk:
            raise ValidationError("An image upload is required for a new product.")
        if image is not None:
            if image.content_type not in ALLOWED_IMAGE_TYPES:
                raise ValidationError("Upload a JPEG, PNG, or WebP image.")
            if image.size > MAX_IMAGE_SIZE:
                raise ValidationError("Product images must be 5 MB or smaller.")
        return image


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ("name", "price", "updated_at")
    search_fields = ("name", "slug", "description")
    ordering = ("name",)

    def save_model(self, request, obj, form, change):
        uploaded_image = form.cleaned_data.get("image_upload")
        old_path = obj.image_path
        if uploaded_image is not None:
            image_path, image_url = upload_product_image(uploaded_image)
            obj.image_path = image_path
            obj.image_url = image_url
        super().save_model(request, obj, form, change)
        if uploaded_image is not None and change and old_path:
            delete_product_image(old_path)

    def delete_model(self, request, obj):
        image_path = obj.image_path
        super().delete_model(request, obj)
        delete_product_image(image_path)

    def delete_queryset(self, request, queryset):
        image_paths = list(queryset.values_list("image_path", flat=True))
        super().delete_queryset(request, queryset)
        for image_path in image_paths:
            delete_product_image(image_path)
