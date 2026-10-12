from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView


class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response(
            {"status": "ok", "service": "elanex-api"},
            status=HTTP_200_OK,
        )


health_check = HealthCheckView.as_view()
