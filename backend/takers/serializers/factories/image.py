from rest_framework.serializers import Serializer
from ..image import ImageToAzureSerializer, ImageToLocalSerializer


class ImageSerializerFactory(Serializer):
    def get_serializer(self, format):
        if format == 'Azure':
            return ImageToAzureSerializer()
        else:
            return ImageToLocalSerializer()
