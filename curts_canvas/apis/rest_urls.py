from django.urls import path, include

from rest_framework import routers

from canvas.rest_views import UserViewSet, PictureViewSet, CustomObtainAuthToken


router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"pictures", PictureViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("authenticate/", CustomObtainAuthToken.as_view()),
    path("api-login/", include("rest_framework.urls")),

]