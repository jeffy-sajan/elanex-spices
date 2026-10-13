from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=160)),
                ("slug", models.SlugField(max_length=180, unique=True)),
                ("description", models.TextField()),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Price for the 100g pack, in Indian rupees.",
                        max_digits=10,
                    ),
                ),
                ("image_url", models.URLField(max_length=500)),
                (
                    "category",
                    models.CharField(
                        choices=[("pods", "Whole cardamom"), ("seeds", "Cardamom seeds")],
                        default="pods",
                        max_length=20,
                    ),
                ),
                ("grade", models.CharField(max_length=120)),
                ("badge", models.CharField(blank=True, max_length=80)),
                ("is_active", models.BooleanField(default=True)),
                ("display_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ("display_order", "name")},
        ),
    ]
