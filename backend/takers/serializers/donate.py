from rest_framework import serializers

from ..models.donate import Donate


class DonateSerializer(serializers.ModelSerializer):
    # not required in calling api
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Donate
        fields = '__all__'
