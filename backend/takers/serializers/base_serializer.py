from rest_framework.serializers import ModelSerializer


class BaseSerializer(ModelSerializer):

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(BaseSerializer, self).get_field_names(
            declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields
