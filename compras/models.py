# ---------------- PANTUFLA 2.0 ------------------
# Sistema desarrollado por Kevin Turkienich 2023
# Contacto: kevin_turkienich@outlook.com
# Garacias por adquirir este producto!
# ----------------------------------------------

# ---------------- IMPORTACIONES DE MODULOS ----------------->
import datetime
from django.db import models
from django.core.exceptions import ValidationError
from inventario.models import Producto
from fabrica.models import Insumo,Compra_insumo
from administracion.models import Proveedor

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
class Compra(models.Model):
    FECHA = models.DateField(default=datetime.date.today)
    CODIGO=models.AutoField(primary_key=True)
    PROVEEDOR = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='compras', blank=True, null=True)
    ARTICULOS = models.ManyToManyField(Producto, through='articulosCompra', related_name='compras_producto', blank=False)
    ESTADO = models.CharField(choices=Estado,default="Pendiente",max_length=50)
    MEDIO_DE_PAGO = models.CharField(choices=Medio_De_Pago,default="Efectivo",max_length=50,blank=False, null=False)
    DETALLES_ADICIONALES = models.TextField(null=True,blank=True)
    COSTO_FINAL = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True, null=True)
    USER = models.CharField(max_length=120,null=True,blank=True)
    
    def calculate_total_cost(self):
        total_cost = 0
        for articulo in self.articuloscompra_set.all():
            total_cost += articulo.cantidad * articulo.precio
        return total_cost

    def clean(self):
        if self.ESTADO == "Controlada":
            raise ValidationError("Las compra se encuentra Controlada, no puede modificarse.")
        super().clean()
        
    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural ='Compras de inventario' 
# ------------------------------------------------------------------
# ------------------------------------------------------------------ 
class articulosCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    insumo = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='articulos_compra')
    cantidad = models.DecimalField(max_digits=20, decimal_places=2, blank=False, null=False, default=1)
    precio = models.DecimalField(verbose_name="Precio Unitario",max_digits=20, decimal_places=2, blank=False, null=False, default=0)
    actualizar_inventario = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.precio = self.precio  # Aquí usamos el precio que has establecido
        super(articulosCompra, self).save(*args, **kwargs)
        self.insumo.PRECIO_COMPRA = self.precio
        self.insumo.save()

    class Meta:
        verbose_name = 'Articulo'
        verbose_name_plural ='Articulos de la compra' 
# ------------------------------------------------------------------
# ------------------------------------------------------------------ 
class Compra_insumo(models.Model):
    FECHA = models.DateField(default=datetime.date.today)
    CODIGO=models.AutoField(primary_key=True)
    PROVEEDOR = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='compras_proveedor', blank=True, null=True)
    INSUMOS = models.ManyToManyField(Insumo,  blank=False)
    ESTADO = models.CharField(choices=Estado,default="Pendiente",max_length=50)
    MEDIO_DE_PAGO = models.CharField(choices=Medio_De_Pago,default="Efectivo",max_length=50,blank=False, null=False)
    DETALLES_ADICIONALES = models.TextField(null=True,blank=True)
    COSTO_FINAL = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True, null=True)
    USER = models.CharField(max_length=120,null=True,blank=True)
    
    def calculate_total_cost(self):
        total_cost = 0
        for articulo in self.insumoscompra_set.all():
            total_cost += articulo.cantidad * articulo.precio
        return total_cost

    def clean(self):
        if self.ESTADO == "Controlada":
            raise ValidationError("Las compra se encuentra Controlada, no puede modificarse.")
        super().clean()

    #def save(self, *args, **kwargs):
    #    if self.ESTADO == "Controlada":
    #        raise ValidationError("La compra está Controlada, no se permite actualizar el precio.")
    #    super(Compra_insumo, self).save(*args, **kwargs)
         
    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural ='Compras de insumos' 
# ------------------------------------------------------------------
# ------------------------------------------------------------------ 
class insumosCompra(models.Model):
    compra = models.ForeignKey(Compra_insumo, on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name='insumos')
    cantidad = models.DecimalField(max_digits=20, decimal_places=2, blank=False, null=False, default=1)
    precio = models.DecimalField(verbose_name="Precio Unitario",max_digits=20, decimal_places=2, blank=False, null=False, default=0)

    def save(self, *args, **kwargs):
        super(insumosCompra, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Insumo'
        verbose_name_plural ='Insumos de la compra' 
# ------------------------------------------------------------------
# ------------------------------------------------------------------ 