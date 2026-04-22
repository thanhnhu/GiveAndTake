from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class UserSerializers(ModelSerializer):
    #password = PasswordField()

    class Meta:
        model = User
        fields = '__all__'

    # encrypt password when creating user
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            # is_staff=validated_data['is_staff']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
