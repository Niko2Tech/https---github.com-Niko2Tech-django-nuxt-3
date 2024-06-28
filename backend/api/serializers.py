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


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    nombre = serializers.CharField(max_length=100)
    direccion = serializers.CharField(max_length=255)
    telefono = serializers.CharField(max_length=20)
    saldo_cuenta = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0.0
    )
