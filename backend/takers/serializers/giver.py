from rest_framework import serializers

from .base_serializer import BaseSerializer
from ..models.giver import Giver


class GiverSerializer(BaseSerializer):
    # not required this field in creating object
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    # declare computed field
    can_edit = serializers.SerializerMethodField(method_name='get_can_edit')
    can_delete = serializers.SerializerMethodField(method_name='get_can_delete')

    class Meta:
        model = Giver
        fields = '__all__'

    def get_can_edit(self, instance):
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            user = request.user
            isOwner = user.is_authenticated and user == instance.user
            isAdmin = user.is_staff
            return isOwner or isAdmin
        return False

    def get_can_delete(self, instance):
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            return request.user.is_superuser
        return False
