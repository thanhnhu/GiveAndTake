from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .base_permissions import IsSuperUser
from ..serializers.factories.image import ImageSerializerFactory


class BaseViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    # set current user as foreign key
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @permission_classes([IsSuperUser])
    def destroy(self, request, pk):
        instance = self.get_object()
        if instance is not None:
            # remove images if there have any
            if hasattr(instance, "images") and instance.images is not None:
                serializer = ImageSerializerFactory.get_serializer(self, settings.STORAGE)
                serializer.remove(instance.id)

            serializer = self.get_serializer(instance)
            data = serializer.data
            self.perform_destroy(instance)
            return Response({'data': data}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
