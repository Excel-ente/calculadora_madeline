# ---------------- PANTUFLA 2.0 ------------------
# Sistema desarrollado por Kevin Turkienich 2023
# Contacto: kevin_turkienich@outlook.com
# Garacias por adquirir este producto!
# ----------------------------------------------

# ---------------- IMPORTACIONES DE MODULOS ----------------->
import datetime
from decimal import Decimal, DivisionByZero
from django.db import models
from django.core.exceptions import ValidationError
from administracion.models import Cliente,Proveedor,Categoria,gastosAdicionales
from django.db.models.signals import post_save
from django.dispatch import receiver
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
Estado_orden = [
    ("Pendiente","Pendiente"),
    ("En curso","En curso"),
    ("Finalizada","Finalizada"),
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

class Insumo(models.Model):
    PRODUCTO = models.CharField(max_length=120, null=False, blank=False)
    PROVEEDOR=models.ForeignKey(Proveedor,on_delete=models.CASCADE,blank=True,null=True)
    DETALLE = models.TextField(null=True, blank=True)
    STOCK = models.IntegerField(default=0,null=True,blank=True)
    CANTIDAD = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    UNIDAD_MEDIDA_COMPRA = models.CharField(max_length=10, choices=UnidadDeMedida, default="Unidades", null=False, blank=False)
    PRECIO_COMPRA = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    UNIDAD_MEDIDA_USO = models.CharField(max_length=10, choices=UnidadDeMedidaSalida, default="Unidades", null=False, blank=False)
    COSTO_UNITARIO = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    PRECIO_VENTA_UNITARIO = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    USER = models.CharField(max_length=120,null=True,blank=True)
    ULTIMA_ACTUALIZACION = models.DateField(default=datetime.date.today)

    class Meta:
        verbose_name = 'Insumo'
        verbose_name_plural ='Insumos' 

    def __str__(self):
        cadena = f'{self.PRODUCTO} (x {self.CANTIDAD} {self.UNIDAD_MEDIDA_COMPRA})'
        return cadena

    def calculate_cost(self):
        if self.PRECIO_COMPRA > 0:
            conversions = {
                "Unidades": 1,
                "Kilogramos": 1000,
                "Litros": 1000,
                "Libras": 16,
                "Onzas": 1,
            }
            conversion_factor = conversions.get(self.UNIDAD_MEDIDA_COMPRA, 1)
            self.COSTO_UNITARIO = self.PRECIO_COMPRA / self.CANTIDAD / conversion_factor

    def convert_units(self):
        conversions = {
            "Kilogramos": "Gramos",
            "Litros": "Mililitros",
            "Libras": "Libras",
            "Onzas": "Onzas",
        }
        self.UNIDAD_MEDIDA_USO = conversions.get(self.UNIDAD_MEDIDA_COMPRA, self.UNIDAD_MEDIDA_USO)

    def save(self, *args, **kwargs):
        self.calculate_cost()
        self.convert_units()

        if self.UNIDAD_MEDIDA_COMPRA == "Kilogramos":
            self.UNIDAD_MEDIDA_USO == "Gramos"
        elif self.UNIDAD_MEDIDA_COMPRA == "Litros":
            self.UNIDAD_MEDIDA_USO == "Mililitros"
        elif self.UNIDAD_MEDIDA_COMPRA == "Onzas":
            self.UNIDAD_MEDIDA_USO == "Onzas"
        elif self.UNIDAD_MEDIDA_COMPRA == "Libras":
            self.UNIDAD_MEDIDA_USO == "Libras"
        elif self.UNIDAD_MEDIDA_COMPRA == "Unidades":
            self.UNIDAD_MEDIDA_USO == "Unidades"
    
        super(Insumo, self).save(*args, **kwargs)
# ------------------------------------------------------------------
# ------------------------------------------------------------------
class Receta(models.Model):
    CODIGO=models.AutoField(verbose_name="LOTE",primary_key=True)
    NOMBRE=models.CharField(verbose_name='PRODUCTO',max_length=120,null=False,blank=False)
    CATEGORIA = models.ForeignKey(Categoria,on_delete=models.CASCADE,blank=True,null=True)
    PORCIONES=models.DecimalField(max_digits=6,decimal_places=2,default=1,blank=False,null=False)
    DETALLE=models.TextField(null=True,blank=True) 
    RENTABILIDAD = models.IntegerField(default=0,blank=True,null=True)
    RENTABILIDAD_POR_PORCION = models.IntegerField(default=0,blank=True,null=True)
    PRECIO_VENTA = models.DecimalField(max_digits=22,decimal_places=2,default=1,blank=False,null=False)
    PRECIO_VENTA_PORCION = models.DecimalField(max_digits=22,decimal_places=2,default=1,blank=False,null=False)
    ADICIONALES = models.ManyToManyField(gastosAdicionales, blank=True)
    INGREDIENTES = models.ManyToManyField(Insumo)
    COSTO_FINAL = models.DecimalField(max_digits=22,decimal_places=2,default=0,blank=True,null=True)
    ULTIMA_ACTUALIZACION = models.DateTimeField(auto_now=True)
    ARTICULOS = models.TextField(blank=True,null=True)
    GASTOS_ADICIONALES = models.DecimalField(verbose_name="TOTAL ADICIONALES",max_digits=22,decimal_places=2,default=0,blank=True,null=True)
    
    USER = models.CharField(max_length=120,null=True,blank=True)

    def __str__(self):
        return f'{self.NOMBRE}'
    
    def clean(self):
        if self.RENTABILIDAD < 0 or self.RENTABILIDAD > 99:
            raise ValidationError("La rentabilidad debe estar contemplada entre el 0% y 99%")
        
        if self.RENTABILIDAD_POR_PORCION < 0 or self.RENTABILIDAD_POR_PORCION > 99:
            raise ValidationError("La rentabilidad por porcion debe estar contemplada entre el 0% y 99%")
        super().clean()

    class Meta:
        verbose_name = 'Receta'
        verbose_name_plural ='Recetas' 

    def save(self, *args, **kwargs):

        if not self.pk:
            super(Receta,self).save(*args, **kwargs)

        costo_receta = 0
        total_gastos_adicionales = 0
        self.COSTO_FINAL = 0

        #Capturar el costo de los insumos
        for ingrediente in self.ingredientereceta_set.all():
            costo_receta += ingrediente.cantidad * ingrediente.costo_unitario

        #Capturar el costo de los gastos adicionales
        for gasto in self.adicionalreceta_set.all():
            total_gastos_adicionales += gasto.precio

        self.GASTOS_ADICIONALES = float(total_gastos_adicionales)

        costo_final = float(total_gastos_adicionales) + float(costo_receta)
        costo_final_porcion = (float(total_gastos_adicionales) + float(costo_receta)) / float(self.PORCIONES)

        self.COSTO_FINAL = costo_final

        if self.RENTABILIDAD > 0 and self.RENTABILIDAD <1000000:
            rentabilidad = float(self.RENTABILIDAD)
            self.PRECIO_VENTA = (costo_final) + ((costo_final) * (rentabilidad / 100))
        else:
            self.PRECIO_VENTA = (costo_final)
        

        if self.RENTABILIDAD_POR_PORCION > 0 and self.RENTABILIDAD_POR_PORCION <1000000:
            rentabilidad = float(self.RENTABILIDAD_POR_PORCION)
            self.PRECIO_VENTA_PORCION = (costo_final_porcion) + ((costo_final_porcion) * (rentabilidad / 100))

        else:
            self.PRECIO_VENTA_PORCION = (costo_final_porcion)
        

        # Generar el texto de los artículos en el formato deseado
        insumos_receta = self.ingredientereceta_set.all()
        articulos = []
        for ingrediente in insumos_receta:
            nombre_producto = ingrediente.producto.PRODUCTO.split(' | $')[0]
            cantidad = ingrediente.cantidad
            u_medida = ingrediente.medida_uso
            precio_unitario = ingrediente.costo_unitario
            precio_total = cantidad * precio_unitario
            articulo = "{} | {} {} | $ {:.2f} | $ {:.2f}".format(nombre_producto, cantidad,u_medida, precio_unitario, precio_total)
            articulos.append(articulo)

        self.ARTICULOS = "\n\n".join(articulos)
        super().save(*args, **kwargs)

    def costo_receta(self):

        total_cost = 0
        costo_receta = 0
        total_gastos_adicionales = 0
        
        # Capturar el costo de los insumos
        for ingrediente in self.ingredientereceta_set.all():
            if ingrediente.costo_unitario is not None:
                costo_receta += ingrediente.cantidad * ingrediente.costo_unitario

        # Capturar el costo de los gastos adicionales
        for gasto in self.adicionalreceta_set.all():
            total_gastos_adicionales += gasto.precio

        total_cost = round((costo_receta + total_gastos_adicionales), 2)

        return total_cost

    def precio_venta(self):

        total = Decimal('0')
        costo_receta = Decimal('0')
        total_gastos_adicionales = Decimal('0')
        rentabilidad = self.RENTABILIDAD

        # Capturar el costo de los insumos
        for ingrediente in self.ingredientereceta_set.all():
            if ingrediente.costo_unitario is not None:
                costo_receta += ingrediente.cantidad * Decimal(str(ingrediente.costo_unitario))

        # Capturar el costo de los gastos adicionales
        for gasto in self.adicionalreceta_set.all():
            total_gastos_adicionales += Decimal(str(gasto.precio))

        total = round((costo_receta + total_gastos_adicionales), 2)

        indice = Decimal(rentabilidad) 

        if rentabilidad > 0 and total > 0:
            try:
                precio_venta = (total / (100-rentabilidad))*100
                #precio_venta = total / (1 - (indice / 100))

            except DivisionByZero:
                precio_venta = Decimal('0')  # O maneja el error de acuerdo a tus necesidades
        else:
            precio_venta = total

        return precio_venta

    def costo_porcion(self):
        total_cost = 0
        costo_receta = 0
        total_gastos_adicionales = 0
        #Capturar el costo de los insumos
        for ingrediente in self.ingredientereceta_set.all():
            costo_receta += ingrediente.cantidad * ingrediente.costo_unitario

        #Capturar el costo de los gastos adicionales
        for gasto in self.adicionalreceta_set.all():
            total_gastos_adicionales += gasto.precio

        total_cost = round(((costo_receta + total_gastos_adicionales) / self.PORCIONES),2)

        return total_cost

    #def deducir_stock(self, cantidad):
    #    for ingrediente in self.ingredientes.all():
    #        insumo = ingrediente.insumo
    #        stock_deductible = ingrediente.cantidad * cantidad
    #        insumo.STOCK -= stock_deductible
    #        insumo.save()
# ------------------------------------------------------------------
# ------------------------------------------------------------------ 
class ingredientereceta(models.Model):

    producto  = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2, default=1, blank=False, null=False)
    costo_unitario = models.DecimalField(max_digits=20, decimal_places=2,blank=True,null=True)
    medida_uso = models.CharField(max_length=255,blank=True,null=True)
    subtotal = models.DecimalField(max_digits=20,decimal_places=2,default=0,blank=False,null=False)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural ='Productos incluidos en la receta' 

    def __str__(self):
        return f'{self.receta.NOMBRE} ({self.producto.UNIDAD_MEDIDA_USO})'
    
    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError("Por favor ingrese una cantidad superior a 0.")
        super().clean()

    def save(self, *args, **kwargs):

        self.costo_unitario = self.producto.COSTO_UNITARIO
        self.medida_uso = self.producto.UNIDAD_MEDIDA_USO
        self.subtotal = self.costo_unitario * self.cantidad

        super(ingredientereceta,self).save(*args, **kwargs)
# ------------------------------------------------------------------
# ------------------------------------------------------------------ 
class adicionalreceta(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    adicional  = models.ForeignKey(gastosAdicionales, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=20, decimal_places=2,blank=False,null=False)
# ------------------------------------------------------------------
# ------------------------------------------------------------------ 
class Compra_insumo(models.Model):
    FECHA = models.DateField(default=datetime.date.today)
    CODIGO=models.AutoField(primary_key=True)
    PROVEEDOR = models.ForeignKey(Proveedor, on_delete=models.CASCADE, blank=True, null=True)
    ESTADO = models.CharField(choices=Estado,default="Pendiente",max_length=50)
    MEDIO_DE_PAGO = models.CharField(choices=Medio_De_Pago,default="Efectivo",max_length=50,blank=False, null=False)
    DETALLES_ADICIONALES = models.TextField(null=True,blank=True)
    ARTICULOS = models.ManyToManyField(Insumo,through='articulosCompra', related_name='articulos_compra', blank=False)
    COSTO_FINAL = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True, null=True)
    USER = models.CharField(max_length=120,null=True,blank=True)
    
    def calculate_total_cost(self):
        total_cost = 0
        for articulo in self.articuloscompra_set.all():
            total_cost += articulo.precio
        return total_cost

    def clean(self):
        if self.ESTADO == "Controlada":
            raise ValidationError("Las compra se encuentra Controlada, no puede modificarse.")
        super().clean()
        
    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural ='Compras de insumos' 
# ------------------------------------------------------------------
# ------------------------------------------------------------------ 
class articulosCompra(models.Model):
    compra = models.ForeignKey(Compra_insumo, on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2, blank=False, null=False, default=1)
    precio = models.DecimalField(max_digits=20, decimal_places=2, blank=False, null=False, default=0)


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
class Orden(models.Model):
    FECHA = models.DateField(default=datetime.date.today)
    CODIGO=models.AutoField(verbose_name="LOTE",primary_key=True)
    CLIENTE = models.ForeignKey(Cliente,on_delete=models.CASCADE,blank=True,null=True)
    ARTICULOS = models.ManyToManyField(Receta, related_name='articulo_orden',related_query_name='articulos', blank=False)
    ESTADO = models.CharField(choices=Estado_orden,default="Pendiente",max_length=50)
    FECHA_ENTREGA = models.DateField()
    DETALLES_ADICIONALES = models.TextField(null=True,blank=True)
    COSTO_FINAL = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True, null=True)
    USER = models.CharField(max_length=120,null=True,blank=True)
    
    def clean(self):
        if self.ESTADO == "Finailizada":
            raise ValidationError("La orden se encuentra finailizada, no puede modificarse.")
        super().clean()
        
    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural ='Ordenes' 

    def costo_orden(self):
        total_cost = 0
        for articulo in self.articulosorden_set.all():
            total_cost += articulo.cantidad * articulo.receta.PRECIO_VENTA
        return total_cost
# ------------------------------------------------------------------
# ------------------------------------------------------------------ 
class articulosOrden(models.Model):
    Orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='receta_orden')
    cantidad = models.DecimalField(max_digits=20, decimal_places=2, blank=False, null=False, default=1)

    def save(self, *args, **kwargs):
        super(articulosOrden, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Articulo'
        verbose_name_plural ='Articulos de la Orden' 
# ------------------------------------------------------------------
# ------------------------------------------------------------------ 
