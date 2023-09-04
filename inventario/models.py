# ---------------- PANTUFLA 2.0 ------------------
# Sistema desarrollado por Kevin Turkienich 2023
# Contacto: kevin_turkienich@outlook.com
# Garacias por adquirir este producto!
# ----------------------------------------------

# ---------------- IMPORTACIONES DE MODULOS ----------------->
import datetime
from django.db import models
from django.core.exceptions import ValidationError
from administracion.models import Proveedor
# ------------------------------------------------------------------

# ---------------------- TABLAS DE DATOS --------------------------------------->
Estado = [
    ("Pendiente","Pendiente"),
    ("Controlada","Controlada"),
]

Medio_De_Pago = [
    ("Efectivo","Efectivo"),
    ("Transferencia","Transferencia"),
    ("Cuenta Corriente","Cuenta Corriente"),
]

# ------------------------------------------------------------------
# ---------------- MODELADO DE BASES DE DATOS --------------------------------->
# ------------------------------------------------------------------
class Categoria(models.Model):
    DESCRIPCION= models.CharField(max_length=120,null=False,blank=False)
    USER = models.CharField(max_length=120,null=True,blank=True)
            
    def __str__(self):
        return self.DESCRIPCION
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural ='Categorias Recetas' 

# ------------------------------------------------------------------
# ------------------------------------------------------------------
class Producto(models.Model):
    PRODUCTO = models.CharField(max_length=120, null=False, blank=False)
    CATEGORIA = models.ForeignKey(Categoria,on_delete=models.CASCADE,blank=True,null=True)
    PROVEEDOR=models.ForeignKey(Proveedor,on_delete=models.CASCADE,blank=True,null=True)
    DETALLE = models.TextField(null=True, blank=True)
    STOCK = models.IntegerField(default=0,null=True,blank=True)
    COSTO = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    PRECIO_VENTA = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    USER = models.CharField(max_length=120,null=True,blank=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural ='Productos' 

    def __str__(self):
        cadena = f'{self.PRODUCTO} ({"$ {:,.2f}".format(self.PRECIO_VENTA)})'
        return cadena

    def save(self, *args, **kwargs):

        super(Producto, self).save(*args, **kwargs)

# ------------------------------------------------------------------
# ------------------------------------------------------------------
