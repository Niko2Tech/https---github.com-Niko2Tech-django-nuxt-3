from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, status
from api.models import *
from api.serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from decimal import Decimal


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()

        if user is None:
            return Response(
                {"error": "Usuario o contraseña incorrecta"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not user.check_password(password):
            return Response(
                {"error": "Usuario o contraseña incorrecta"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)

        # Buscamos el nombre del cliente asociado al usuario
        cliente = Cliente.objects.filter(usuario=user).first()

        return Response(
            {
                "access": str(refresh.access_token),
                "username": user.username,
                "cliente": cliente.nombre if cliente else None,
                "direccion": cliente.direccion if cliente else "",
                "saldo": cliente.saldo_cuenta if cliente else "",
                "user_id": user.id,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            password_confirmation = serializer.validated_data["password_confirmation"]
            nombre = serializer.validated_data["nombre"]
            direccion = serializer.validated_data["direccion"]
            telefono = serializer.validated_data["telefono"]
            saldo_cuenta = serializer.validated_data["saldo_cuenta"]

            if User.objects.filter(username=email).exists():
                return Response(
                    {"error": "El correo electrónico ya está en uso."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.create_user(
                username=email, email=email, password=password
            )

            cliente = Cliente.objects.create(
                nombre=nombre,
                direccion=direccion,
                telefono=telefono,
                email=email,
                saldo_cuenta=saldo_cuenta,
                usuario=user,
            )
            cuenta_cliente = CuentaCliente.objects.create(
                cliente=cliente, saldo=saldo_cuenta
            )
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "detail": "Usuario registrado exitosamente",
                    "access": str(refresh.access_token),
                    "username": user.username,
                    "user_id": user.id,
                    "cliente": cliente.nombre,
                    "direccion": cliente.direccion,
                    "saldo": cliente.saldo_cuenta,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def check_auth(self, request):
        token = request.data.get("token")
        try:
            access_token = AccessToken(token)
            user_id = access_token.get("user_id")
            user = User.objects.get(id=user_id)

            # Buscamos el nombre del cliente asociado al usuario
            cliente = Cliente.objects.filter(usuario=user).first()

            return Response(
                {
                    "detail": "Token válido",
                    "username": user.username,
                    "user_id": user.id,
                    "cliente": cliente.nombre if cliente else None,
                    "direccion": cliente.direccion if cliente else "",
                    "saldo": cliente.saldo_cuenta if cliente else "",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": "Token inválido", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["post"])
    def logout(self, request):
        return Response({"detail": "Sesión cerrada"}, status=status.HTTP_200_OK)


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["get"])
    def productos_oferta(self, request):
        queryset = Producto.objects.filter(oferta=True)
        serializer = ProductoSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # productos ordenados por el nombre de su categoria
    @action(detail=False, methods=["get"])
    def productos_categoria(self, request):
        categorias = Categoria.objects.all()
        response_data = []

        for categoria in categorias:
            productos = Producto.objects.filter(categoria=categoria)
            productos_serializados = ProductoSerializer(productos, many=True).data
            response_data.append(
                {"nombre": categoria.nombre, "productos": productos_serializados}
            )

        return Response(response_data, status=status.HTTP_200_OK)


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"])
    def generar_pedido(self, request):
        serializer = PedidoCreateSerializer(data=request.data)
        if serializer.is_valid():
            pedido = serializer.save()
            response_serializer = PedidoSerializer(pedido)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def pedidos_usuario(self, request):
        pk = request.query_params.get("user_id")
        # buscamos al usuario por su id
        user = User.objects.get(id=pk)
        # buscamos al cliente asociado al usuario
        cliente = Cliente.objects.get(usuario=user)
        # buscamos los pedidos asociados al cliente
        pedidos = Pedido.objects.filter(cliente=cliente).order_by("-fecha")
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetallePagoViewSet(viewsets.ModelViewSet):
    queryset = DetallePago.objects.all()
    serializer_class = DetallePagoSerializer
    permission_classes = [permissions.AllowAny]


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"])
    def agregar_saldo(self, request):
        # buscamos el user id en los parametros de la petición
        user_id = request.data.get("user_id")
        # validamos que el usuario exista
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response(
                {"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )
        # buscamos el cliente asociado al usuario
        cliente = Cliente.objects.get(usuario=user_id)
        # buscamos el saldo a agregar
        saldo = request.data.get("saldo_cuenta")
        # validamos el saldo
        if saldo <= 0:
            return Response(
                {"error": "El saldo a agregar debe ser mayor a 0"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # agregamos el saldo al cliente
        cliente.saldo_cuenta += Decimal(saldo)
        cliente.save()
        # retornamos el saldo actualizado
        return Response({"saldo": cliente.saldo_cuenta}, status=status.HTTP_200_OK)
