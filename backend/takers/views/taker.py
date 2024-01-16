from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count
from django.db.models import Q

from .base_permissions import IsOwnerOrIsAdminOrReadOnly
from .base_pagination import BasePagination
from .base_view import BaseViewSet
from ..models.taker import Taker
from ..serializers.taker import TakerSerializer


class TakerViewSet(BaseViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrIsAdminOrReadOnly]

    serializer_class = TakerSerializer
    pagination_class = BasePagination
    #queryset = Taker.objects.all().order_by('date_created')

    def get_queryset(self):
        curUser = self.request.user

        querySet = None
        if curUser.is_authenticated == True:
            isMine = self.request.query_params.get('isMine')
            if isMine is not None and isMine.lower() in ['true']:
                querySet = Taker.objects.filter(Q(user=curUser))
            else:
                querySet = Taker.objects.filter(Q(user=curUser) | Q(stop_donate=False))
        else:
            querySet = Taker.objects.filter(stop_donate=False)

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

        # order by total donate least first, then date created soonest
        # TODO: should use Sum instead of Count
        return querySet.annotate(total=Count('donates')).order_by('total', 'date_created')

    @action(detail=True, methods=['patch'])
    def stop_donate(self, request, pk):
        taker = Taker.objects.get(id=pk)
        if taker is not None:
            taker.stop_donate = not taker.stop_donate
            taker.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
