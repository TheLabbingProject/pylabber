"""
Definition of the :class:`ExportDestinationViewSet` class.
"""
from accounts.filters import ExportDestinationFilter
from accounts.models.export_destination import ExportDestination
from accounts.serializers.export_destination import ExportDestinationSerializer
from accounts.tasks import export_mri_session
from pylabber.views.defaults import DefaultsMixin
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

EXPORT_HANDLERS: dict = {"django_mri": {"Session": export_mri_session}}


class ExportDestinationViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows
    :class:`~accounts.models.export_destination.ExportDestination` instances to
    be viewed or edited.
    """

    queryset = ExportDestination.objects.order_by("id")
    serializer_class = ExportDestinationSerializer
    filter_class = ExportDestinationFilter

    @action(detail=True, methods=["GET"])
    def export_instance(
        self,
        request: Request,
        pk: int,
        app_label: str,
        model_name: str,
        instance_id: int,
    ):
        handler = EXPORT_HANDLERS.get(app_label, {}).get(model_name)
        if handler:
            try:
                handler.delay(pk, instance_id, **self.request.GET)
            except AttributeError:
                handler(pk, instance_id, **self.request.GET)
            finally:
                return Response(status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)
