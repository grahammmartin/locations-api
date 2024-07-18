from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from .models import LocationRequest
from .serializers import (
    AddressLocationRequestSerializer,
    BaseLocationRequestSerializer,
)


class LocationViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = LocationRequest.objects.all()
    serializer_class = BaseLocationRequestSerializer

    @action(detail=False, methods=["post"], serializer_class=AddressLocationRequestSerializer)
    def get_geocode(self, request):
        serializer = AddressLocationRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

