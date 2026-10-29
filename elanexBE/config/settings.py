import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "development-only-change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"

if not DEBUG and (
    not os.getenv("DJANGO_SECRET_KEY")
    or SECRET_KEY == "development-only-change-me"
):
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY must be set when DJANGO_DEBUG is False."
    )

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "localhost,127.0.0.1" if DEBUG else "",
    ).split(",")
    if host.strip()
]
if not DEBUG and not ALLOWED_HOSTS:
    raise ImproperlyConfigured(
        "DJANGO_ALLOWED_HOSTS must contain at least one host when DJANGO_DEBUG is False."
    )

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "core",
]

JAZZMIN_SETTINGS = {
    "site_title": "Elanex Spices Admin",
    "site_header": "Elanex Spices",
    "site_brand": "Elanex Spices",
    "welcome_sign": "Welcome to the Elanex Spices administration",
    "copyright": "Elanex Spices",
    "show_ui_builder": False,
    "navigation_expanded": True,
    "changeform_format": "horizontal_tabs",
    "related_modal_active": True,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "sidebar_nav_small_text": False,
    "button_small_text": False,
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_flat_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_compact_style": False,
    "brand_colour": "navbar-success",
    "accent": "accent-success",
    "navbar_fixed": True,
    "sidebar_fixed": True,
    "footer_fixed": False,
    "layout_boxed": False,
    "actions_sticky_top": True,
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASE_URL = os.getenv("DATABASE_URL")
if not DEBUG and not DATABASE_URL:
    raise ImproperlyConfigured(
        "DATABASE_URL must be set when DJANGO_DEBUG is False."
    )

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}" if DEBUG else None,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        (
            "http://localhost:3000,http://localhost:5173,"
            "http://localhost:8080,http://localhost:8081"
            if DEBUG
            else ""
        ),
    ).split(",")
    if origin.strip()
]
if not DEBUG and not CORS_ALLOWED_ORIGINS:
    raise ImproperlyConfigured(
        "CORS_ALLOWED_ORIGINS must contain the deployed frontend origin when DJANGO_DEBUG is False."
    )
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]
if not DEBUG and not CSRF_TRUSTED_ORIGINS:
    raise ImproperlyConfigured(
        "CSRF_TRUSTED_ORIGINS must contain the deployed frontend origin when DJANGO_DEBUG is False."
    )

STATIC_ROOT = BASE_DIR / "staticfiles"

SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
if SUPABASE_URL.endswith("/rest/v1"):
    SUPABASE_URL = SUPABASE_URL[: -len("/rest/v1")]
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
SUPABASE_STORAGE_BUCKET = os.getenv(
    "SUPABASE_STORAGE_BUCKET",
    "product-images",
)
USE_PRODUCT_CATALOG_FILE = os.getenv("USE_PRODUCT_CATALOG_FILE", "true").lower() == "true"

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
CONTACT_RECIPIENT_EMAIL = os.getenv(
    "CONTACT_RECIPIENT_EMAIL",
    "elanexspices@gmail.com",
)
CONTACT_FROM_EMAIL = os.getenv("CONTACT_FROM_EMAIL", "")

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "contact": "5/minute",
    },
}

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "{levelname} {asctime} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
        "core": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}
