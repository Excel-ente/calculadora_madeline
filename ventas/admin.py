# ---------------- PANTUFLA 2.0 ------------------
# Sistema desarrollado por Kevin Turkienich 2023
# Contacto: kevin_turkienich@outlook.com
# Garacias por adquirir este producto!
# ----------------------------------------------


# ---------------- IMPORTACIONES DE MODULOS ----------------->

from django.contrib import admin
from .models import Venta,articulosVenta
#from administracion.Funciones import Autorizar
from import_export.admin import ImportExportModelAdmin

# ---------------- TITULO DEL SITIO ----------------->

admin.site.site_header = "Gestion Pantu"
admin.site.site_title = "Gestion Pantu"

# ---------------- ADMINISTRACION DE MODELOS  ----------------->

class articulosVentaInline(admin.TabularInline):
    model = articulosVenta
    extra = 1
    fields = ('insumo', 'cantidad', 'precio')

class VentaAdmin(admin.ModelAdmin):

    inlines = [
        articulosVentaInline,
    ]

    list_display = ('FECHA','ESTADO','MEDIO_DE_PAGO','CLIENTE','Total',)
    ordering = ('FECHA',)
    exclude = ('USER','COSTO_FINAL','ESTADO')
    list_per_page = 50
    search_fields=('CLIENTE', )
    list_display_links = ('CLIENTE','FECHA',)
    #actions = [Autorizar,]

    def Total(self,obj):
        formateo = "$ {:,.2f}".format(obj.COSTO_FINAL)
        return formateo
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)

# ---------------- REGISTRACION DE MODULOS ----------------->

admin.site.register(Venta, VentaAdmin)