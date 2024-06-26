from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import *


# Serializador de la tabla User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


# Serializador de producto
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = "__all__"
