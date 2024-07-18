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


class PedidoCreateSerializer(serializers.Serializer):
    estado = serializers.ChoiceField(choices=Pedido.CHOISE_ESTADO)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())
    tipo_entrega = serializers.CharField(max_length=50)
    direccion_entrega = serializers.CharField(max_length=255)
    productos = serializers.ListField(
        child=serializers.DictField(child=serializers.IntegerField())
    )
    metodo_pago = serializers.ChoiceField(choices=DetallePago.CHOISE_METODO_PAGO)
    monto = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        metodo_pago = validated_data.pop("metodo_pago")
        monto = validated_data.pop("monto")
        productos = validated_data.pop("productos")

        pedido = Pedido.objects.create(**validated_data)

        for producto_data in productos:
            producto_id = producto_data["id"]
            cantidad = producto_data["cantidad"]
            producto = Producto.objects.get(id=producto_id)
            precio_unitario = producto.precio
            if producto.porcentaje_descuento:
                precio_unitario = precio_unitario * (1 - producto.porcentaje_descuento)
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
            )

        DetallePago.objects.create(pedido=pedido, metodo_pago=metodo_pago, monto=monto)

        # creamos la ruta de entrega
        repartidor = Repartidor.objects.filter(estado="disponible").first()
        if repartidor:
            RutaEntrega.objects.create(
                repartidor=repartidor, pedido=pedido, estado="pendiente"
            )
            repartidor.estado = "ocupado"
            repartidor.save()

        # buscamos el saldo del modelo cliente
        cliente = Cliente.objects.get(id=validated_data["cliente"].id)
        # si el monto es mayor al saldo de la cuenta del cliente dejamos la cuenta del cliente en 0 y si el monto es menor restamos el monto al saldo de la cuenta del cliente
        if cliente.saldo_cuenta >= monto:
            cliente.saldo_cuenta -= monto
        else:
            cliente.saldo_cuenta = 0
        cliente.save()

        return pedido


class DetallePedidoSerializer(serializers.ModelSerializer):
    # nombre del producto
    producto = serializers.CharField(source="producto.nombre")
    imagen = serializers.CharField(source="producto.imagen")

    class Meta:
        model = DetallePedido
        fields = ["producto", "cantidad", "precio_unitario", "imagen"]


class PedidoSerializer(serializers.ModelSerializer):
    productos_con_cantidad = DetallePedidoSerializer(
        many=True, source="detallepedido_set"
    )

    class Meta:
        model = Pedido
        fields = [
            "id",
            "fecha",
            "estado",
            "total",
            "cliente",
            "tipo_entrega",
            "direccion_entrega",
            "productos_con_cantidad",
            "repartidor",
            "fecha_actualizacion",
        ]


class DetallePagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePago
        fields = "__all__"


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"


class CuentaClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaCliente
        fields = "__all__"
