from django.urls import include, path
from rest_framework import routers
from .views import *

# router de rest_framework
routers = routers.DefaultRouter()
routers.register("api/user", UserViewSet, "user")
routers.register("api/producto", ProductoViewSet, "producto")
routers.register("api/pedido", PedidoViewSet, "pedido")
routers.register("api/detallepago", DetallePagoViewSet, "detallepago")
routers.register("api/cliente", ClienteViewSet, "cliente")


urlpatterns = routers.urls
