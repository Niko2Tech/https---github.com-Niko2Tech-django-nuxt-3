from django.db import models

# modelo usuario de django
from django.contrib.auth.models import User


class Administrador(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    saldo_cuenta = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class CuentaCliente(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    historial_pedido = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultimo_pedido = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.cliente.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, null=True, blank=True
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponibilidad = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    oferta = models.BooleanField(default=False)
    porcentaje_descuento = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )
    imagen = models.ImageField(upload_to="productos/", null=True, blank=True)

    # texto que se muestra en el admin
    def __str__(self):
        return self.nombre + " - " + str(self.precio)


class Pedido(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_entrega = models.CharField(max_length=50)
    direccion_entrega = models.CharField(max_length=255)
    productos = models.ManyToManyField(Producto)
    repartidor = models.ForeignKey(
        "Repartidor", null=True, blank=True, on_delete=models.SET_NULL
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)


class Repartidor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    estado = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class RutaEntrega(models.Model):
    repartidor = models.ForeignKey(Repartidor, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
