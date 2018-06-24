from django.contrib.auth.models import User

from rest_framework import viewsets, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from apis.serializers import UserSerializer, PictureSerializer
from .models import Picture


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


# Method returns JWT token for use if user login information is valid
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data["token"])
        user = User.objects.get(id=token.user_id)
        serializer = UserSerializer(user, many= False)
        return Response({
            "token": token.key, "user": serializer.data
        })
