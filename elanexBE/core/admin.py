import logging

from django import forms
from django.contrib import admin, messages
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.http import HttpResponseRedirect

from .models import Product
from .storage import (
    ALLOWED_IMAGE_TYPES,
    MAX_IMAGE_SIZE,
    StorageOperationError,
    delete_product_image,
    storage_is_configured,
    upload_product_image,
)

logger = logging.getLogger(__name__)


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
            if not storage_is_configured():
                raise ValidationError(
                    "Supabase Storage is not configured. Add SUPABASE_URL and "
                    "SUPABASE_SERVICE_ROLE_KEY to elanexBE/.env, then restart Django."
                )
            if image.content_type not in ALLOWED_IMAGE_TYPES:
                raise ValidationError("Upload a JPEG, PNG, or WebP image.")
            if image.size > MAX_IMAGE_SIZE:
                raise ValidationError("Product images must be 5 MB or smaller.")
        return image


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ("name", "category", "price", "updated_at")
    list_filter = ("category",)
    search_fields = ("name", "slug", "description")
    ordering = ("name",)

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        try:
            return super().changeform_view(
                request, object_id, form_url, extra_context
            )
        except (ImproperlyConfigured, StorageOperationError) as error:
            self.message_user(
                request,
                f"Product image operation failed: {error}",
                messages.ERROR,
            )
            return HttpResponseRedirect(request.path)
        except DatabaseError:
            self.message_user(
                request,
                "The product could not be saved because of a database error.",
                messages.ERROR,
            )
            return HttpResponseRedirect(request.path)
        except ValidationError:
            self.message_user(
                request,
                (
                    "The product could not be saved because one or more "
                    "values are invalid."
                ),
                messages.ERROR,
            )
            return HttpResponseRedirect(request.path)

    def save_model(self, request, obj, form, change):
        uploaded_image = form.cleaned_data.get("image_upload")
        old_path = obj.image_path
        new_path = ""
        if uploaded_image is not None:
            new_path, image_url = upload_product_image(uploaded_image)
            obj.image_path = new_path
            obj.image_url = image_url
        try:
            super().save_model(request, obj, form, change)
        except (DatabaseError, ValidationError):
            if new_path:
                try:
                    delete_product_image(new_path)
                except (ImproperlyConfigured, StorageOperationError):
                    logger.exception(
                        "Could not remove uploaded image after product save failed: %s",
                        new_path,
                    )
            raise
        if uploaded_image is not None and change and old_path:
            try:
                delete_product_image(old_path)
            except (ImproperlyConfigured, StorageOperationError) as error:
                self.message_user(
                    request,
                    f"Product saved, but the previous image could not be removed: {error}",
                    messages.WARNING,
                )

    def delete_model(self, request, obj):
        image_path = obj.image_path
        super().delete_model(request, obj)
        try:
            delete_product_image(image_path)
        except (ImproperlyConfigured, StorageOperationError) as error:
            self.message_user(
                request,
                f"Product deleted, but its image could not be removed: {error}",
                messages.WARNING,
            )

    def delete_queryset(self, request, queryset):
        image_paths = list(queryset.values_list("image_path", flat=True))
        super().delete_queryset(request, queryset)
        for image_path in image_paths:
            try:
                delete_product_image(image_path)
            except (ImproperlyConfigured, StorageOperationError) as error:
                self.message_user(
                    request,
                    f"Products deleted, but an image could not be removed: {error}",
                    messages.WARNING,
                )
