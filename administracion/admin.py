# ---------------- PANTUFLA 2.0 ------------------
# Sistema desarrollado por Kevin Turkienich 2023
# Contacto: kevin_turkienich@outlook.com
# Garacias por adquirir este producto!
# ----------------------------------------------

# ---------------- IMPORTACIONES DE MODULOS ----------------->

from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# ---------------- TITULO DEL SITIO ----------------->

admin.site.site_header = "Pantufla"
admin.site.site_title = "Pantufla"

# ---------------- ADMINISTRACION DE MODELOS  ----------------->

class CategoriaAdmin(admin.ModelAdmin):
    list_display=('DESCRIPCION',)
    exclude=('USER',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)

class ConfiguracionAdmin(ImportExportModelAdmin):
    list_display = ('estado','NOMBRE_EMPRESA','DIRECCION','TELEFONO','EMAIL','LOGO',)
    exclude=('USER',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)

class ProveedorAdmin(ImportExportModelAdmin):
    list_display = ('EMPRESA', 'NOMBRE','DIRECCION', 'EMAIL','TELEFONO',)
    ordering = ('NOMBRE',)
    search_fields = ('EMPRESA','NOMBRE',)
    list_filter = ('EMPRESA',)
    exclude=('USER',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)

class ClienteAdmin(ImportExportModelAdmin):
    list_display = ('CODIGO', 'NOMBRES','EMAIL', 'TELEFONO',)
    ordering = ('NOMBRES',)
    search_fields = ('CODIGO','NOMBRES',)
    exclude=('USER',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)

class InventarioAdmin(ImportExportModelAdmin):
    list_display = ('Producto','PROVEEDOR', 'COSTO_POR_UNIDAD','COSTO_TOTAL','STOCK',)
    ordering = ('PRODUCTO',)
    list_filter=('PROVEEDOR',)
    exclude=('COSTO_UNITARIO','UNIDAD_MEDIDA_USO','STOCK','PRECIO_VENTA_UNITARIO','PRECIO_VENTA','USER')
    search_fields = ('PRODUCTO', 'PROVEEDOR__EMPRESA',)

    list_per_page = 50
    list_display_links = ('Producto',)


    def COSTO_TOTAL(self, obj):
        return "💲{:,.2f}".format(obj.PRECIO_COMPRA)
    
    def PRECIO_VENTA(self, obj):
        return "💲{:,.2f}".format(obj.PRECIO_VENTA_UNITARIO)
    
    def COSTO_POR_UNIDAD(self, obj):

        costo_unitario = obj.COSTO_UNITARIO
        unidad_medida = obj.UNIDAD_MEDIDA_USO
        costo_formateado = f'💲{costo_unitario:,.2f}'

        cadena = f'{costo_formateado} x {unidad_medida}'

        return cadena
        
    def Producto(self, obj):

        cadena = f'{obj.PRODUCTO} (x{obj.CANTIDAD} {obj.UNIDAD_MEDIDA_COMPRA})'
        
        return cadena

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)

class gastosAdicionalesAdmin(ImportExportModelAdmin):
    list_display=('PRODUCTO',)
    ordering = ('PRODUCTO',)
    search_fields = ('PRODUCTO',)
    exclude=('USER',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["CATEGORIA", "PROVEEDOR"]:
            kwargs["queryset"] = db_field.related_model.objects.filter(USER=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

# ---------------- REGISTRACION DE MODULOS ----------------->

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Configuracion, ConfiguracionAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(gastosAdicionales,gastosAdicionalesAdmin)