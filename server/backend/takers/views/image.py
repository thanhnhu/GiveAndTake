import os
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from ..serializers.factories.image import ImageSerializerFactory
from .base_permissions import PostOrReadOnly
from ..models.taker import Taker
from ..models.giver import Giver


class ImageViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [PostOrReadOnly]
    serializer_class = ImageSerializerFactory

    def create(self, request, *args, **kwargs):
        supported_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        files = request.data.getlist("files")
        # validate files first
        for file in files:
            if file.content_type not in supported_types:
                return Response({"error": "100", "message": "Need images file"}, status=status.HTTP_400_BAD_REQUEST)
            if file.size > 1024 * 1024 * 10:
                return Response({"error": "101", "message": "File size > 10MB"}, status=status.HTTP_400_BAD_REQUEST)

        # get hostname from environment of docker compose
        hostname = os.environ.get('HOST_NAME') if os.environ.get('HOST_NAME') is not None else request.get_host()
        host = request.scheme + "://" + hostname
        id = request.data.get("id")
        isTaker = bool(request.data.get("isTaker"))
        isGiver = bool(request.data.get("isGiver"))

        factory = self.get_serializer()
        serializer = factory.get_serializer(settings.STORAGE)
        result = serializer.save(host, id, files)

        # save to owner
        if isTaker == True:
            taker = Taker.objects.get(id=id)
            if taker is not None:
                if not taker.images:
                    taker.images = result
                else:
                    taker.images += result
                taker.save()
        elif isGiver == True:
            giver = Giver.objects.get(id=id)
            if giver is not None:
                if not giver.images:
                    giver.images = result
                else:
                    giver.images += result
                giver.save()

        return Response(result, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        factory = self.get_serializer()
        serializer = factory.get_serializer(settings.STORAGE)
        result = serializer.load(pk, "abc")
        return Response(result)
