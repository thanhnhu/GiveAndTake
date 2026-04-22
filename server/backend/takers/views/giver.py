from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .base_permissions import IsOwnerOrIsAdminOrReadOnly
from .base_pagination import BasePagination
from .base_view import BaseViewSet
from ..models.giver import Giver
from ..serializers.giver import GiverSerializer


class GiverViewSet(BaseViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrIsAdminOrReadOnly]

    serializer_class = GiverSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        curUser = self.request.user

        querySet = None
        if curUser.is_authenticated == True:
            isMine = self.request.query_params.get('isMine')
            if isMine is not None and isMine.lower() in ['true']:
                querySet = Giver.objects.filter(Q(user=curUser))
            else:
                querySet = Giver.objects.filter(Q(user=curUser) | Q(active=True))
        else:
            querySet = Giver.objects.filter(active=True)

        city = self.request.query_params.get('city')
        if city is not None and city and not city.isspace():
            querySet = querySet.filter(city=city)

        number = self.request.query_params.get('number')
        if number is not None and number and not number.isspace():
            querySet = querySet.filter(number=number)

        name = self.request.query_params.get('name')
        if name is not None and name and not name.isspace():
            querySet = querySet.filter(name__icontains=name)

        phone = self.request.query_params.get('phone')
        if phone is not None and phone and not phone.isspace():
            querySet = querySet.filter(phone__contains=phone)

        # order by date created latest first
        return querySet.order_by('-date_created')

    @action(detail=True, methods=['patch'])
    def set_active(self, request, pk):
        giver = Giver.objects.get(id=pk)
        if giver is not None:
            giver.active = not giver.active
            giver.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
