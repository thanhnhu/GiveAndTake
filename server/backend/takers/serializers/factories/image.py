from rest_framework.serializers import Serializer
from ..image import ImageToGoogleDriveSerializer, ImageToAzureSerializer, ImageToLocalSerializer


class ImageSerializerFactory(Serializer):
    def get_serializer(self, format):
        if format == 'Google':
            return ImageToGoogleDriveSerializer()
        elif format == 'Azure':
            return ImageToAzureSerializer()
        else:
            return ImageToLocalSerializer()
