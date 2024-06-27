from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, status
from api.models import *
from api.serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["get"])
    def productos_oferta(self, request):
        queryset = Producto.objects.filter(oferta=True)
        serializer = ProductoSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # productos ordenados por categoria
    @action(detail=False, methods=["get"])
    def productos_categoria(self, request):
        queryset = Producto.objects.order_by("categoria")
        serializer = ProductoSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
