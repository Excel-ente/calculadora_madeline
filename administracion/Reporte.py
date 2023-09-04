from django.http import HttpResponse
from reportlab.lib.pagesizes import letter,legal
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from django.contrib import admin, messages
from .models import Configuracion
import os
import locale
from django.core.files.storage import default_storage

def get_configuracion(usuario):
    # Buscar la configuración activa del usuario
    configuracion = Configuracion.objects.filter(USER=usuario, estado=True).first()

    # Si no hay configuración activa, buscar una inactiva
    if not configuracion:
        configuracion = Configuracion.objects.filter(USER="kevin", estado=True).first()

    return configuracion

@admin.action(description="Descargar Receta")
def generar_presupuesto(modeladmin, request, queryset):

    #Validacion para que seleccione solo 1 queryset
    if len(queryset) != 1:
        messages.error(request, "Seleccione solo un pedido para generar el informe.")
        return
      
    #Capturo la ruta actual para la ruta del logo
    current_directory = os.getcwd()

    logo_path = os.path.join(current_directory, 'static/logo.png')
    
    # Obtener el primer pedido seleccionado
    pedido = queryset[0]
    nombre_empresa = "EXCEL-ENTE"
    direccion_empresa = "Calculadora de costos 2.1v"
    telefono_empresa = "Fecha de actualizacion 27/08/2023"
    email_empresa = "turkienich@excel-ente.net"
    

    usuario = pedido.USER
    configuracion = get_configuracion(usuario)

    if configuracion:

        nombre_empresa = configuracion.NOMBRE_EMPRESA
        direccion_empresa = configuracion.DIRECCION
        telefono_empresa = configuracion.TELEFONO
        email_empresa = configuracion.EMAIL

        logo_path = configuracion.LOGO.path if configuracion.LOGO else None

  

    # Establecer el idioma en español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    # Obtener el primer pedido seleccionado
    pedido = queryset[0]  
    #Crear el objeto
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="presupuesto_{pedido.CODIGO}.pdf"'
    # Crear el lienzo PDF
    p = canvas.Canvas(response, pagesize=legal)

    # Agregar contenido al lienzo
    y = 950  # Posición vertical inicial
    x = 50
        # Verificar si el archivo de imagen del logo existe
    if logo_path:
        # Tamaño y posición del logo
        logo_width = 150  # Ancho del logo
        logo_height = 150 # Alto del logo
        logo_x = 410  # Posición horizontal del logo
        logo_y = 820  # Posición vertical del logo

        # Agregar el logo al lienzo PDF
        logo_image = ImageReader(logo_path)
        p.drawImage(logo_image, logo_x, logo_y, width=logo_width, height=logo_height)
    
 
    # Titulo del reporte
    p.setFont("Helvetica-Bold", 18)  
    p.drawString(x, y, nombre_empresa)
    y -= 20

    p.setFont("Helvetica", 12)  # Fuente normal
    p.drawString(x, y, direccion_empresa)
    y -= 15

    p.drawString(x, y, telefono_empresa)
    y -= 15

    p.drawString(x, y, email_empresa)
    y -= 15

    # Seccion de cliente - Titulo
    p.setFont("Helvetica-Bold", 12)  # Fuente en negrita y tamaño 14
    p.drawString(x, y, f"")
    y -= 20

    # Bloque entrega
    p.setFillColorRGB(0, 0, 0)  # Color de texto negro
    p.setFont("Helvetica-Bold", 12)  # Fuente en negrita y tamaño 14
    p.drawString(x, y, f"DATOS DE LA RECETA")
    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Receta #: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str(pedido.CODIGO)
    p.drawString(100, y, codigo_str.zfill(4))
    y -= 15

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Porciones por receta: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str(pedido.PORCIONES)
    p.drawString(160, y, codigo_str)
    y -= 15

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Costo Porcion: $ ")
    p.setFont("Helvetica", 10)  # Fuente normal
    Calculo = pedido.costo_porcion()
    codigo_str = str("{:,.2f}".format(Calculo))
    p.drawString(160, y, codigo_str)
    y -= 15

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Costo Total: $ ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str("{:,.2f}".format(pedido.costo_receta()))
    p.drawString(130, y, codigo_str)
    y -= 25



    # Dividir el detalle en líneas utilizando "#"
    detalle = str(pedido.DETALLE)
    posicion_x = 50
    lineas = detalle.split("\n")

    
    contador = 0

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "DETALLES ADICIONALES: ")
    y -= 20

    p.setFont("Helvetica", 10)

    for linea in lineas:

        largo = len(linea)

        if largo > 1:
            linea = linea[:largo-1]
            p.drawString(posicion_x, y, linea)
            y -= 20
        else:
            p.drawString(posicion_x, y, "Sin Adicionales.")
            y -= 20


    # Obtener los gastos adicionales de la receta
    gastos_adicionales = pedido.adicionalreceta_set.all()

    if gastos_adicionales:
        p.setFont("Helvetica-Bold", 10)  # Fuente en negrita y tamaño 14
        p.drawString(x, y, f"COSTOS ADICIONALES:")
        y -= 20
        for gasto in gastos_adicionales:
            p.setFont("Helvetica", 10)  # Fuente en negrita
            p.drawString(x, y, f"{gasto.adicional.PRODUCTO}: $ {gasto.precio:,.2f}")
            y -= 20

    y -= 10
    # Bloque entrega
    p.setFillColorRGB(0, 0, 0)  # Color de texto negro
    p.setFont("Helvetica-Bold", 13)  # Fuente en negrita y tamaño 14
    p.drawString(x, y, f"INSUMOS INCLUIDOS EN LA RECETA")
    y -= 25

    p.setFont("Helvetica", 10)  
    p.setFillColorRGB(0, 0, 0)  # Color de texto negro

    articulos = pedido.ARTICULOS.split("\n\n")

    columna_actual = 1  # Variable para controlar la columna actual
    y_inicial = y  # Guardar la posición vertical inicial
    for i, articulo in enumerate(articulos):
        if i % 23 == 0 and i > 0:
            # Cambiar a la siguiente columna
            columna_actual += 1
            y = y_inicial
        p.drawString(x + 270 * (columna_actual - 1), y, f"• {articulo.strip()}")
        y -= 20


    y = 60
    p.setFont("Helvetica-Bold", 14)
    p.drawString(280, y, "Precio total Presupuestado: ")
    p.setFont("Helvetica", 13)  # Fuente normal
    p.drawString(480, y,  f'$ {pedido.PRECIO_VENTA:,.2f}')
    y -= 40

    p.save()

    return response




@admin.action(description="Descargar detalle de Presupuesto")
def generar_reporte_cliente(modeladmin, request, queryset):

    #Validacion para que seleccione solo 1 queryset
    if len(queryset) != 1:
        messages.error(request, "Seleccione solo un pedido para generar el informe.")
        return
    #Capturo la ruta actual para la ruta del logo
    current_directory = os.getcwd()
    #el logo esta en la raiz del proyecto
    logo_path = os.path.join(current_directory, 'static/logo.png')
    # Establecer el idioma en español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    # Obtener el primer pedido seleccionado
    pedido = queryset[0]  
    #Crear el objeto
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Presupuesto_det_{pedido.CODIGO}.pdf"'
    # Crear el lienzo PDF
    p = canvas.Canvas(response, pagesize=legal)

    # Agregar contenido al lienzo
    y = 950  # Posición vertical inicial
    x = 50
        # Verificar si el archivo de imagen del logo existe
    if logo_path:
        # Tamaño y posición del logo
        logo_width = 130  # Ancho del logo
        logo_height = 130  # Alto del logo
        logo_x = 420  # Posición horizontal del logo
        logo_y = 830  # Posición vertical del logo
        # Agregar el logo al lienzo PDF
        p.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height)
    
    # Titulo del reporte
    p.setFont("Helvetica-Bold", 16)  
    p.drawString(x, y, f"DETALLE DEL PRESUPUESTO")
    y -= 15
    #Redes sociales
    p.setFont("Helvetica-Bold", 10)
    y -= 20
    # Seccion de cliente - Titulo
    p.setFont("Helvetica-Bold", 12)  # Fuente en negrita y tamaño 14
    p.drawString(x, y, f"DATOS DEL CLIENTE")
    y -= 20

    # Numero de cliente
    p.setFont("Helvetica-Bold", 10)  # Fuente en negrita
    p.drawString(x, y, "Cliente #: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    p.drawString(100, y, str(pedido.CLIENTE.NUMERO_CLIENTE))
    y -= 20

    # Nombre y apellido
    p.setFont("Helvetica-Bold", 10)  # Fuente en negrita
    p.drawString(x, y, "Nombre y apellido: ")
    p.setFont("Helvetica", 10)
    p.drawString(150, y, str(pedido.CLIENTE.NOMBRE_Y_APELLIDO))
    y -= 20

    p.setFont("Helvetica-Bold", 10)  # Fuente en negrita
    p.drawString(x, y, "Direccion: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    p.drawString(105, y, str(pedido.CLIENTE.DIRECCION))
    y -= 20

    # Email
    p.setFont("Helvetica-Bold", 10)  # Fuente en negrita
    p.drawString(x, y, "Email: ")
    p.setFont("Helvetica", 10)
    p.drawString(90, y, str(pedido.CLIENTE.EMAIL))
    y -= 20

    # Telefono
    p.setFont("Helvetica-Bold", 10)  # Fuente en negrita
    p.drawString(x, y, "Telefono: ")
    p.setFont("Helvetica", 10)
    p.drawString(100, y, str(pedido.CLIENTE.TELEFONO))
    y -= 40


    # Bloque entrega
    p.setFillColorRGB(0, 0, 0)  # Color de texto negro
    p.setFont("Helvetica-Bold", 12)  # Fuente en negrita y tamaño 14
    p.drawString(x, y, f"DETALLE DEL PRODUCTO:")
    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Presupuesto #: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str(pedido.CODIGO)
    p.drawString(130, y, codigo_str.zfill(4))
    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Fecha de entrega: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    p.drawString(140, y,  f"{pedido.FECHA_ENTREGA.strftime('%A %d de %B del %Y')}")
    y -= 20

    #Detalle de pedido
    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "DETALLES: ")
    y -= 20 
    p.setFont("Helvetica", 10)  # Fuente normal
    detalle = str(pedido.DETALLE)
    posicion_x = 50

    # Dividir el detalle en líneas utilizando "#"
    lineas = detalle.split("\n")

    for linea in lineas:
        # Mostrar la línea en el lienzo PDF
        largo = len(linea)
        linea = linea[:largo-1]
        p.drawString(posicion_x, y, linea)
        # Ajustar la posición vertical para la siguiente línea
        y -= 20

    # Bloque adicionales
    # Sección de gastos adicionales
    p.setFont("Helvetica-Bold", 10)  # Fuente en negrita y tamaño 14
    p.drawString(x, y, f"COSTOS ADICIONALES:")
    y -= 20

    # Obtener los gastos adicionales de la receta
    gastos_adicionales = pedido.adicionalreceta_set.all()

    for gasto in gastos_adicionales:
        p.setFont("Helvetica", 10)  # Fuente en negrita
        p.drawString(x, y, f"{gasto.adicional.PRODUCTO}: $ {gasto.precio:,.2f}")
        y -= 20

    y -= 10
    # Bloque entrega
    p.setFillColorRGB(0, 0, 0)  # Color de texto negro
    p.setFont("Helvetica-Bold", 10)  # Fuente en negrita y tamaño 14
    p.drawString(x, y, f"MATERIALES UTILIZADOS:")
    y -= 25
    
    p.setFont("Helvetica", 10)  
    p.setFillColorRGB(0, 0, 0)  # Color de texto negro

    articulos = pedido.ARTICULOS.split(", ")

    columna_actual = 1  # Variable para controlar la columna actual
    y_inicial = y  # Guardar la posición vertical inicial
    for i, articulo in enumerate(articulos):
        if i % 20 == 0 and i > 0:
            # Cambiar a la siguiente columna
            columna_actual += 1
            y = y_inicial
        p.drawString(x + 270 * (columna_actual - 1), y, f"• {articulo.strip()} Unid.")
        y -= 20


    y = 40
    p.setFont("Helvetica-Bold", 14)
    p.drawString(280, y, "Precio total Presupuestado: ")
    p.setFont("Helvetica", 13)  # Fuente normal
    p.drawString(480, y,  f'$ {pedido.PRECIO_VENTA:,.2f}')
    y -= 40


    p.save()

    return response
