# ---------------- PANTUFLA 2.0 ------------------
# Sistema desarrollado por Kevin Turkienich 2023
# Contacto: kevin_turkienich@outlook.com
# Garacias por adquirir este producto!
# ----------------------------------------------

# ---------------- IMPORTACIONES DE MODULOS ----------------->

from django.contrib import admin
from fabrica.models import *
from import_export.admin import ImportExportModelAdmin
from administracion.Funciones import Actualizar
from administracion.Reporte import generar_presupuesto
# ---------------- TITULO DEL SITIO ----------------->

admin.site.site_header = "Pantufla"
admin.site.site_title = "Pantufla"

# ---------------- ADMINISTRACION DE MODELOS  ----------------->


class InsumoAdmin(ImportExportModelAdmin):
    list_display = ('Nombre_de_producto','PROVEEDOR','Costo','Stock_actual')
    ordering = ('PRODUCTO',)
    list_filter = ('PROVEEDOR',)
    exclude = ('COSTO_UNITARIO','STOCK', 'UNIDAD_MEDIDA_USO', 'ULTIMA_ACTUALIZACION','PRECIO_VENTA_UNITARIO','USER')
    list_per_page = 50
    search_fields=('PRODUCTO',)
    list_display_links = ('Nombre_de_producto',)

    def Stock_actual(seld,obj):
        return f'{obj.STOCK} {obj.UNIDAD_MEDIDA_COMPRA}'
    
    def Nombre_de_producto(self,obj):
        formateo = f'{obj.PRODUCTO} x{obj.CANTIDAD} {obj.UNIDAD_MEDIDA_COMPRA}'
        return formateo

    def Costo(self, obj):
        formateo = "$ {:,.2f}".format(obj.PRECIO_COMPRA)
        return formateo
    
    def Ultima_Actualizacion(self, obj): 
        fecha_hora = obj.ULTIMA_ACTUALIZACION
        formateo = fecha_hora.strftime("%H:%M %d/%m/%Y")

        formateo = "📆 " +formateo
        return formateo
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)
 
class IngredienteRecetaInline(admin.TabularInline):
    model = ingredientereceta
    extra = 1
    readonly_fields = ('medida_uso',)
    fields = ('producto', 'cantidad','medida_uso')

class gastosAdicionalesInline(admin.TabularInline):
    model = adicionalreceta
    extra = 1
    fields = ('adicional', 'precio',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "adicional":
            kwargs["queryset"] = gastosAdicionales.objects.filter(USER=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)   
   
class RecetaAdmin(admin.ModelAdmin):

    inlines = [
        gastosAdicionalesInline,
        IngredienteRecetaInline,
    ]

    list_display = ('NOMBRE','CATEGORIA','Costo_Receta','Rentabilidad','Precio_de_venta','Ultima_Actualizacion',)#'FECHA_ACTUALIZACION'
    ordering = ('NOMBRE',)
    list_filter = ('CATEGORIA',)
    exclude = ('ADICIONALES','GASTOS_ADICIONALES','ARTICULOS','STOCK', 'INGREDIENTES', 'ULTIMA_ACTUALIZACION', 'PRECIO_VENTA_PORCION','PRECIO_VENTA', 'COSTO_FINAL','USER')
    list_per_page = 50
    search_fields=('NOMBRE', )
    list_display_links = ('NOMBRE',)
    actions = [Actualizar, generar_presupuesto]

    def Rentabilidad(self, obj):
        formateo = "% {:,.2f}".format(obj.RENTABILIDAD)
        return formateo

    def Costo_Receta(self, obj):  
        formateo = "💲{:,.2f}".format(obj.costo_receta())
        return formateo

    def Precio_de_venta(self, obj):  
        formateo = "💲{:,.2f}".format(obj.precio_venta())
        return formateo
    
    def Ultima_Actualizacion(self, obj): 
        fecha_hora = obj.ULTIMA_ACTUALIZACION
        formateo = fecha_hora.strftime("%H:%M %d/%m/%Y")

        formateo = "📆 " +formateo
        return formateo
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)
 
class articulosOrdenInline(admin.TabularInline):
    model = articulosOrden
    extra = 1
    fields = ('receta', 'cantidad',)

class OrdenAdmin(ImportExportModelAdmin):

    inlines = [
        articulosOrdenInline,
    ]

    list_display = ('CLIENTE','ESTADO','FECHA_ENTREGA','Total_pedido',)
    ordering = ('FECHA',)
    list_filter = ('CLIENTE','ESTADO',)
    exclude=('COSTO_FINAL','USER','ARTICULOS','ESTADO','FECHA',)
    search_fields = ('ARTICULOS','CODIGO')
    actions=['Fabricar',]
    list_per_page = 50

    def Total_pedido(self, obj):  
        formateo = "💲{:,.2f}".format(obj.costo_orden())
        return formateo
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)

    
    def Fabricar(self, request, queryset):
        contador = 0
        for orden in queryset:
            if orden.ESTADO != "Finalizada" and orden.ESTADO != "En curso":
                recetas = orden.ARTICULOS.all()  # Accede a las recetas asociadas a la orden
                for receta in recetas:
                    receta.deducir_stock(orden.cantidad)  # Llama al método deducir_stock en la receta
                orden.ESTADO = "Finalizada"
                orden.save()
                contador += 1
            else:
                self.message_user(request, f"La orden #{orden.pk} ya está fabricada.")

        if contador > 0:
            self.message_user(request, f"Se ha creado el lote de fabricación para {contador} órdenes.")



admin.site.register(Orden, OrdenAdmin)
admin.site.register(Insumo, InsumoAdmin)
admin.site.register(Receta, RecetaAdmin)