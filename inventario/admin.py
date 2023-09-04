# ---------------- PANTUFLA 2.0 ------------------
# Sistema desarrollado por Kevin Turkienich 2023
# Contacto: kevin_turkienich@outlook.com
# Garacias por adquirir este producto!
# ----------------------------------------------

# ---------------- IMPORTACIONES DE MODULOS ----------------->

from django.contrib import admin
from inventario.models import Producto
from import_export.admin import ImportExportModelAdmin

# ---------------- TITULO DEL SITIO ----------------->

admin.site.site_header = "Pantufla"
admin.site.site_title = "Pantufla"

# ---------------- ADMINISTRACION DE MODELOS  ----------------->

class ProductoAdmin(ImportExportModelAdmin):
    list_display = ('PRODUCTO','CATEGORIA','PROVEEDOR','PRECIO_VENTA','STOCK',)
    list_filter=('PROVEEDOR',)
    exclude=('COSTO_UNITARIO','STOCK','COSTO','USER')
    search_fields = ('PRODUCTO', 'PROVEEDOR__EMPRESA',)

    list_per_page = 50
    list_display_links = ('PRODUCTO',)


    #def COSTO_TOTAL(self, obj):
     #   return "💲{:,.2f}".format(obj.PRECIO_COMPRA)


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)

admin.site.register(Producto, ProductoAdmin)