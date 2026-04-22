from rest_framework.authentication import TokenAuthentication

from .base_permissions import IsOwnerOrIsAdminOrReadOnly, PostOrReadOnly
from .base_view import BaseViewSet
from ..models.donate import Donate
from ..serializers.donate import DonateSerializer


class DonateViewSet(BaseViewSet):
    authentication_classes = [TokenAuthentication]
    # work in python old version
    permission_classes = [IsOwnerOrIsAdminOrReadOnly | PostOrReadOnly]
    http_method_names = ['post', 'patch', 'delete']

    serializer_class = DonateSerializer
    queryset = Donate.objects.all().order_by('date_created')
