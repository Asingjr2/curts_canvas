from django.contrib.auth.models import User

from rest_framework import viewsets, generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import list_route
from rest_framework.response import Response
from apis.serializers import UserSerializer, PictureSerializer, RatingSerializer
from .models import Picture, Rating


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    @list_route(methods=["POST"])
    def rate_picture(self, request):
        if "picture" in request.data and "user" in request.data and "stars" in request.data:
            user = User.objects.get(id=request.data["user"])
            picture = Picture.objects.get(id=request.data["picture"])
            stars = int(request.data["stars"])

            # Creating logic to differentiate updates versus creates w/ response values
            try:
                my_rating = Rating.objects.get(movie=picture.id, user=user.id)
                my_rating.stars = stars
                my_rating.save()
                serializer = PictureSerializer(picture, many=False)
                response = {"message":"Rating updated","result": serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                Rating.objects.create(picture=picture, user=user, stars=stars)
                my_rating = Rating.objects.get(picture=picture.id, user=user.id)
                my_rating.stars = stars
                my_rating.save()
                serializer = PictureSerializer(picture, many=False)
                response = {"message":"Rating created","result": serializer.data}
                return Response(response, status=status.HTTP_200_OK)
          
        else:
            response = {"message": "You need to pass all params"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)




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
