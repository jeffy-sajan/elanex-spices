from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    class Category(models.TextChoices):
        PODS = "pods", "Whole cardamom"
        SEEDS = "seeds", "Cardamom seeds"

    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price for the 100g pack, in Indian rupees.",
    )
    image_url = models.URLField(max_length=500)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.PODS,
    )
    grade = models.CharField(max_length=120)
    badge = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("display_order", "name")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
