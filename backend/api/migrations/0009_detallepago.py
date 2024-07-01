# Generated by Django 5.0.6 on 2024-06-28 20:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_remove_cuentacliente_historial_pedido_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetallePago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('metodo_pago', models.CharField(max_length=50)),
                ('pedido', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.pedido')),
            ],
        ),
    ]