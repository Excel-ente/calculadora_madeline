# ---------------- PANTUFLA 2.0 ------------------
# Sistema desarrollado por Kevin Turkienich 2023
# Contacto: kevin_turkienich@outlook.com
# Garacias por adquirir este producto!
# ----------------------------------------------

# ---------------- IMPORTACIONES DE MODULOS ----------------->
import datetime
from django.db import models
from django.core.exceptions import ValidationError

# ------------------------------------------------------------------
# ---------------- MODELADO DE BASES DE DATOS --------------------------------->

class Configuracion(models.Model):
    estado=models.BooleanField(verbose_name="ACTIVO",default=False)
    NOMBRE_EMPRESA= models.CharField(max_length=120,null=True,blank=True)
    DIRECCION=models.CharField(max_length=255,null=True,blank=True)
    TELEFONO =models.CharField(max_length=255,null=True,blank=True)          
    EMAIL=models.CharField(max_length=255,null=True,blank=True)
    LOGO= models.ImageField(upload_to='logos/',null=True,blank=True)
    USER = models.CharField(max_length=120,null=True,blank=True)
    
    class Meta:
        verbose_name = 'Mis Datos'
        verbose_name_plural = 'Mis Datos'
# ------------------------------------------------------------------
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
class Proveedor(models.Model):
    EMPRESA=models.CharField(max_length=120,null=False,blank=False) 
    NOMBRE=models.CharField(max_length=120,null=False,blank=False) 
    DIRECCION=models.CharField(max_length=120,null=True,blank=True)
    EMAIL=models.EmailField(null=True,blank=True)
    TELEFONO=models.CharField(max_length=120,null=False,blank=False)
    USER = models.CharField(max_length=120,null=True,blank=True)

    def __str__(self):
        return self.EMPRESA
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural ='Proveedores' 
# ------------------------------------------------------------------
# ------------------------------------------------------------------
class Cliente(models.Model):
    CODIGO=models.CharField(max_length=120,null=False,blank=False) 
    NOMBRES=models.CharField(max_length=120,null=True,blank=True)
    EMAIL=models.EmailField(null=True,blank=True)
    TELEFONO=models.CharField(max_length=120,null=False,blank=False)
    USER = models.CharField(max_length=120,null=True,blank=True)

    def __str__(self):
        return self.NOMBRES
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural ='Clientes' 
# ------------------------------------------------------------------
# ------------------------------------------------------------------
class gastosAdicionales(models.Model):
    PRODUCTO  = models.CharField(max_length=255,blank=False,null=False)
    USER = models.CharField(max_length=120,null=True,blank=True)

    def __str__(self):
        return self.PRODUCTO
# ------------------------------------------------------------------
# ------------------------------------------------------------------  