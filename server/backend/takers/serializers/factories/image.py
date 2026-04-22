from rest_framework.serializers import Serializer
from ..image import ImageToCloudinarySerializer, ImageToGoogleDriveSerializer, ImageToAzureSerializer, ImageToLocalSerializer


class ImageSerializerFactory(Serializer):
    def get_serializer(self, format):
        if format == 'Google':
            return ImageToGoogleDriveSerializer()
        elif format == 'Azure':
            return ImageToAzureSerializer()
        elif format == 'Cloudinary':
            return ImageToCloudinarySerializer()
        else:
            return ImageToLocalSerializer()
