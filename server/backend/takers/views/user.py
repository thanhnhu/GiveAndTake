from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
import json

from .base_permissions import IsOwnerOrIsAdmin, DeleteDenied
from ..serializers.user import UserSerializers


class CustomObtainAuthToken(ObtainAuthToken):
    # authenticate
    def post(self, request, *args, **kwargs):
        #serializer = self.serializer_class(data=request.data, context={'request': request})
        # serializer.is_valid(raise_exception=True)
        #user = serializer.validated_data['user']
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.values('username', 'email', 'first_name', 'last_name', 'is_staff').get(id=token.user_id)
        data = json.dumps(user)
        return Response({'token': token.key, 'user': data})


class UserViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrIsAdmin & DeleteDenied]
    http_method_names = ['get', 'post', 'patch']
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get_permissions(self):
        # allow Anonymous to create new user
        if self.request.method == 'POST':
            return []

        return super().get_permissions()
