# ---------------- PANTUFLA 2.0 ------------------
# Sistema desarrollado por Kevin Turkienich 2023
# Contacto: kevin_turkienich@outlook.com
# Garacias por adquirir este producto!
# ----------------------------------------------


# ---------------- IMPORTACIONES DE MODULOS ----------------->

from django.contrib import admin
from .models import insumosCompra,Compra,Compra_insumo,articulosCompra
from import_export.admin import ImportExportModelAdmin

# ---------------- TITULO DEL SITIO ----------------->

admin.site.site_header = "Gestion Pantu"
admin.site.site_title = "Gestion Pantu"

# ---------------- ADMINISTRACION DE MODELOS  ----------------->

class articulosCompraInline(admin.TabularInline):
    model = articulosCompra
    extra = 1
    fields = ('insumo', 'cantidad', 'precio')

class CompraAdmin(admin.ModelAdmin):

    inlines = [
        articulosCompraInline,
    ]

    list_display = ('FECHA','ESTADO','MEDIO_DE_PAGO','PROVEEDOR','Costo_Total',)
    ordering = ('FECHA',)
    exclude = ('USER','COSTO_FINAL','ESTADO')
    list_per_page = 50
    search_fields=('PROVEEDOR', )
    list_display_links = ('FECHA',)

    def Costo_Total(self,obj):
        formateo = "$ {:,.2f}".format(obj.calculate_total_cost())
        return formateo
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)

class insumosCompraInline(admin.TabularInline):
    model = insumosCompra
    extra = 1
    fields = ('insumo', 'cantidad', 'precio')

class CompraInsumoAdmin(admin.ModelAdmin):

    inlines = [
        insumosCompraInline,
    ]

    list_display = ('FECHA','ESTADO','MEDIO_DE_PAGO','PROVEEDOR','Costo_Total',)
    ordering = ('FECHA',)
    exclude = ('USER','COSTO_FINAL','INSUMOS','ESTADO')
    list_per_page = 50
    search_fields=('PROVEEDOR', )
    list_display_links = ('PROVEEDOR','FECHA',)
    actions = ["Controlar",]
    
    def Costo_Total(self,obj):
        formateo = "$ {:,.2f}".format(obj.calculate_total_cost())
        return formateo
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)

    def Controlar(self, request, queryset):
        contador=0
        for compra in queryset:
            if compra.ESTADO != "Controlada":
                insumos_compra = insumosCompra.objects.filter(compra=compra)
                for insumo_compra in insumos_compra:
                    insumo = insumo_compra.insumo
                    cantidad = insumo_compra.cantidad
                    insumo.STOCK += cantidad
                    insumo.PRECIO_COMPRA = insumo_compra.precio
                    insumo.save()
                compra.ESTADO = "Controlada"
                compra.save()
                contador += 1
            else:
                self.message_user(request, f"La compra #{compra.pk} ya está controlada.")

        if contador > 0:
            self.message_user(request, "El stock de los insumos ha sido actualizado desde las compras seleccionadas.")

# ---------------- REGISTRACION DE MODULOS ----------------->

admin.site.register(Compra, CompraAdmin)
admin.site.register(Compra_insumo, CompraInsumoAdmin)