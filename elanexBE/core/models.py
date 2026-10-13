from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify


class Product(models.Model):
    class Category(models.TextChoices):
        CARDAMOM = "cardamom", "Cardamom"
        SEEDS = "seeds", "Seeds"

    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Price in Indian rupees.",
    )
    image_url = models.URLField(max_length=500)
    image_path = models.CharField(max_length=500, blank=True)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.CARDAMOM,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at", "id")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)[:180]
            candidate = base_slug
            suffix = 2
            while Product.objects.filter(slug=candidate).exists():
                suffix_text = f"-{suffix}"
                candidate = f"{base_slug[:180 - len(suffix_text)]}{suffix_text}"
                suffix += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
