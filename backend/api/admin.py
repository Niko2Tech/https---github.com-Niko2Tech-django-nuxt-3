from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Administrador)
admin.site.register(Proveedor)
admin.site.register(Cliente)
admin.site.register(CuentaCliente)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(Repartidor)
admin.site.register(RutaEntrega)
admin.site.register(DetallePedido)
