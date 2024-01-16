from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from ..models.city import City
from ..serializers.city import CitySerializer


class CityViewSet(ListModelMixin, GenericViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
