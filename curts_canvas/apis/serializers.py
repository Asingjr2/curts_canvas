from django.contrib.auth.models import User 

from rest_framework import serializers

from canvas.models import Picture


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "email")
        extra_kwargs = { "password": { "write_only": True, "required": True}}

    def create(self, validated_data): 
        user = User.objects.create_user(**validated_data)
        return user


class PictureSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Picture
        fields = ("id", "name", "description", "price")
        lookup_field = "pk"