from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, status
from api.models import *
from api.serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


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
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "username": user.username,
                "cliente": cliente.nombre if cliente else None,
                "direccion": cliente.direccion if cliente else "",
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def check_auth(self, request):
        token = request.data.get("token")
        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            user = User.objects.get(id=user_id)

            # Buscamos el nombre del cliente asociado al usuario
            cliente = Cliente.objects.filter(usuario=user).first()

            return Response(
                {
                    "detail": "Token válido",
                    "username": user.username,
                    "cliente": cliente.nombre if cliente else None,
                    "direccion": cliente.direccion if cliente else "",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": "Token inválido", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
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
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "username": user.username,
                    "cliente": cliente.nombre,
                    "direccion": cliente.direccion,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def logout(self, request):
        # eliminamos el token de acceso
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()
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
