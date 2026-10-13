import json
import logging
from urllib import error as urllib_error
from urllib import request as urllib_request

from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_502_BAD_GATEWAY
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .models import Product

logger = logging.getLogger(__name__)

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
        try:
            products = Product.objects.all()
            product_data = [
                {
                    "id": product.slug,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "image": product.image_url,
                    "category": product.category,
                }
                for product in products
            ]
        except DatabaseError:
            logger.exception("Product catalogue request failed")
            return Response(
                {"detail": "The product catalogue is temporarily unavailable."},
                status=503,
            )
        return Response(
            product_data,
            status=HTTP_200_OK,
        )


products_list = ProductListView.as_view()


class ContactMessageView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "contact"

    def post(self, request):
        name = str(request.data.get("name", "")).strip()
        email = str(request.data.get("email", "")).strip()
        message = str(request.data.get("message", "")).strip()

        if not name or len(name) > 120:
            return Response({"detail": "Enter a valid name."}, status=HTTP_400_BAD_REQUEST)
        try:
            validate_email(email)
        except ValidationError:
            return Response({"detail": "Enter a valid email address."}, status=HTTP_400_BAD_REQUEST)
        if not message or len(message) > 5000:
            return Response({"detail": "Enter a message up to 5,000 characters."}, status=HTTP_400_BAD_REQUEST)
        if not settings.RESEND_API_KEY or not settings.CONTACT_FROM_EMAIL:
            return Response({"detail": "Contact email service is not configured."}, status=HTTP_502_BAD_GATEWAY)

        payload = json.dumps(
            {
                "from": settings.CONTACT_FROM_EMAIL,
                "to": [settings.CONTACT_RECIPIENT_EMAIL],
                "reply_to": [email],
                "subject": f"New website enquiry from {name}",
                "text": f"Name: {name}\nEmail: {email}\n\n{message}",
            }
        ).encode("utf-8")
        email_request = urllib_request.Request(
            "https://api.resend.com/emails",
            data=payload,
            headers={
                "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                "Content-Type": "application/json",
                "User-Agent": "Elanex-Spices-Contact-Form/1.0",
            },
            method="POST",
        )
        try:
            with urllib_request.urlopen(email_request, timeout=10) as response:
                if response.status < 200 or response.status >= 300:
                    raise urllib_error.HTTPError(
                        email_request.full_url, response.status, "Resend rejected the email", response.headers, None
                    )
        except (urllib_error.HTTPError, urllib_error.URLError, TimeoutError):
            logger.exception("Contact email provider request failed")
            return Response({"detail": "We could not send your message. Please try again."}, status=HTTP_502_BAD_GATEWAY)

        return Response({"detail": "Your message has been sent."}, status=HTTP_200_OK)


contact_message = ContactMessageView.as_view()
