# ---------------- PANTUFLA 2.0 ------------------
# Sistema desarrollado por Kevin Turkienich 2023
# Contacto: kevin_turkienich@outlook.com
# Garacias por adquirir este producto!
# ----------------------------------------------

# ---------------- IMPORTACIONES DE MODULOS ----------------->
import datetime
from django.db import models
from django.core.exceptions import ValidationError
from administracion.models import Cliente
from inventario.models import Producto

# ------------------------------------------------------------------

# ---------------------- TABLAS DE DATOS --------------------------------------->
UnidadDeMedida = [
    ("Unidades","Unidades"),
    ("Kilogramos","Kilogramos"),
    ("Litros","Litros"),
    ("Onzas","Onzas"),
    ("Libras","Libras"),
]
Estado = [
    ("Pendiente","Pendiente"),
    ("Controlada","Controlada"),
]
Medio_De_Pago = [
    ("Efectivo","Efectivo"),
    ("Transferencia","Transferencia"),
    ("Cuenta Corriente","Cuenta Corriente"),
]
UnidadDeMedidaSalida = [
    ("Unidades","Unidades"),
    ("Gramos","Gramos"),
    ("Mililitros","Mililitros"),
    ("Onzas","Onzas"),
    ("Libras","Libras"),
]
# ------------------------------------------------------------------
# ---------------- MODELADO DE BASES DE DATOS --------------------------------->

# ------------------------------------------------------------------ 
class Venta(models.Model):
    FECHA = models.DateField(default=datetime.date.today)
    CODIGO=models.AutoField(primary_key=True)
    CLIENTE = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='Ventas_proveedor', blank=True, null=True)
    ARTICULOS = models.ManyToManyField(Producto, through='articulosVenta', related_name='articulos_venta', blank=False)
    ESTADO = models.CharField(choices=Estado,default="Pendiente",max_length=50)
    MEDIO_DE_PAGO = models.CharField(choices=Medio_De_Pago,default="Efectivo",max_length=50,blank=False, null=False)
    DETALLES_ADICIONALES = models.TextField(null=True,blank=True)
    COSTO_FINAL = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True, null=True)
    USER = models.CharField(max_length=120,null=True,blank=True)
    
    def calculate_total_cost(self):
        total_cost = 0
        for articulo in self.articulosVenta_set.all():
            total_cost += articulo.precio
        return total_cost

    def clean(self):
        if self.ESTADO == "Controlada":
            raise ValidationError("Las Venta se encuentra Controlada, no puede modificarse.")
        super().clean()
        
    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural ='Ventas de insumos' 
# ------------------------------------------------------------------
# ------------------------------------------------------------------ 
class articulosVenta(models.Model):
    Venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    insumo = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='ventas_insumo')
    cantidad = models.DecimalField(max_digits=20, decimal_places=2, blank=False, null=False, default=1)
    precio = models.DecimalField(verbose_name="Precio Total",max_digits=20, decimal_places=2, blank=False, null=False, default=0)

    def save(self, *args, **kwargs):
        super(articulosVenta, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Articulo'
        verbose_name_plural ='Articulos de la Venta' 
# ------------------------------------------------------------------
# ------------------------------------------------------------------ 