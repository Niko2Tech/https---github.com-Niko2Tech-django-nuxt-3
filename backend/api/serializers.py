from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Menu


# Serializador de la tabla Menu
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


# Serializador de la tabla User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
