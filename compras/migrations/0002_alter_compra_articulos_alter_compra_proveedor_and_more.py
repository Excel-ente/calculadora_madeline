# Generated by Django 4.2.2 on 2023-08-27 13:25

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fabrica', '0002_alter_adicionalreceta_adicional_and_more'),
        ('inventario', '0002_remove_compra_articulos_remove_compra_proveedor_and_more'),
        ('administracion', '0002_gastosadicionales_alter_cliente_options'),
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='ARTICULOS',
            field=models.ManyToManyField(related_name='compras_producto', through='compras.articulosCompra', to='inventario.producto'),
        ),
        migrations.AlterField(
            model_name='compra',
            name='PROVEEDOR',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='compras', to='administracion.proveedor'),
        ),
        migrations.CreateModel(
            name='insumosCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, default=1, max_digits=20)),
                ('precio', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Precio Total')),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compras.compra')),
                ('insumo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insumos', to='fabrica.insumo')),
            ],
            options={
                'verbose_name': 'Insumo',
                'verbose_name_plural': 'Insumos de la compra',
            },
        ),
        migrations.CreateModel(
            name='Compra_insumo',
            fields=[
                ('FECHA', models.DateField(default=datetime.date.today)),
                ('CODIGO', models.AutoField(primary_key=True, serialize=False)),
                ('ESTADO', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Controlada', 'Controlada')], default='Pendiente', max_length=50)),
                ('MEDIO_DE_PAGO', models.CharField(choices=[('Efectivo', 'Efectivo'), ('Transferencia', 'Transferencia'), ('Cuenta Corriente', 'Cuenta Corriente')], default='Efectivo', max_length=50)),
                ('DETALLES_ADICIONALES', models.TextField(blank=True, null=True)),
                ('COSTO_FINAL', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=22, null=True)),
                ('USER', models.CharField(blank=True, max_length=120, null=True)),
                ('INSUMOS', models.ManyToManyField(to='fabrica.insumo')),
                ('PROVEEDOR', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='compras_proveedor', to='administracion.proveedor')),
            ],
            options={
                'verbose_name': 'Compra',
                'verbose_name_plural': 'Compras de insumos',
            },
        ),
    ]
