from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import *
import re


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
    password_confirmation = serializers.CharField(write_only=True)
    nombre = serializers.CharField(max_length=100)
    direccion = serializers.CharField(max_length=255)
    telefono = serializers.CharField(max_length=20)
    saldo_cuenta = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0.0
    )

    def validate(self, data):
        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("El email ya existe")
        # validamos el numero de telefono con regex
        if not re.match(r"^\+56\d{9}$", data["telefono"]):
            raise serializers.ValidationError(
                "El telefono no es valido (Ej: +56912345678)"
            )
        return data
