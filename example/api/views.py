from rest_framework import viewsets

from drf_aggregates.renderers import AggregateRenderer

from rest_framework.response import Response
from example.models import Car, Manufacturer
from example.api.serializers import CarSerializer, ManufacturerSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_fields = (
        'classification',
        'is_bullet_proof',
    )

    def list(self, request, *args, **kwargs):
        renderer = request.accepted_renderer
        if isinstance(renderer, AggregateRenderer):
            queryset = self.filter_queryset(self.get_queryset())
            data = request.accepted_renderer.render({'queryset': queryset, 'request': request})
            return Response(data, content_type=f'application/json')
        return super().list(request, *args, **kwargs)


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

