from rest_framework import serializers

from .base_serializer import BaseSerializer
from .donate import DonateSerializer
from ..models.taker import Taker


class TakerSerializer(BaseSerializer):
    # not required this field in creating object
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    # get related list
    donates = DonateSerializer(many=True, read_only=True)
    # declare computed field
    can_edit = serializers.SerializerMethodField(method_name='get_can_edit')
    can_delete = serializers.SerializerMethodField(method_name='get_can_delete')

    class Meta:
        model = Taker
        fields = '__all__'
        #extra_fields = ['donates']

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
