from fileinput import filename
from django.http import HttpResponse
from reportlab.pdfgen.canvas import Canvas
from datetime import datetime, timedelta
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, PageBreak, \
    PageTemplate, Spacer, FrameBreak, NextPageTemplate, Image
from reportlab.lib.pagesizes import letter,A4
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER,TA_LEFT,TA_RIGHT




class Vendedor:
    """
    Información del Vendedor: Nombre, sucursal, meta de venta
    """
    def __init__(self, nombre_vendedor, sucursal, dia_reporte):
        self.nombre_vendedor = nombre_vendedor
        self.sucursal = sucursal
        self.dia_reporte = dia_reporte


class Actividades:
    """
    Información de las Actividades realizadas: Hora de actividad y duración, cliente atendido,
    tipo de actividad, resultado, monto venta (mxn) + (usd), monto cotización (mxn) + (usd),
    solicitud de apoyo y comentarios adicionales
    """
    def __init__(self, hora_actividad, duracion_actividad, cliente, tipo_actividad, resultado,
                 monto_venta_mxn, monto_venta_usd, monto_cot_mxn, monto_cot_usd, requiero_apoyo, comentarios_extra):
        self.hora_actividad = hora_actividad
        self.duracion_actividad = duracion_actividad
        self.cliente = cliente
        self.tipo_actividad = tipo_actividad
        self.resultado = resultado
        self.monto_venta_mxn = monto_venta_mxn
        self.monto_venta_usd = monto_venta_usd
        self.monto_cot_mxn = monto_cot_mxn
        self.monto_cot_usd = monto_cot_usd
        self.requiero_apoyo = requiero_apoyo
        self.comentarios_extra = comentarios_extra

class PDFReport:
    """
    Crea el Reporte de Actividades diarias en archivo de formato PDF
    """
    def __init__(self, filename):
        self.filename = filename


def total_report(pk):
    vendedor = Vendedor('John Doe', 'Stack Overflow', datetime.now().strftime('%d/%m/%Y'))

    file_name = 'cronograma_actividades.pdf'
    document_title = 'Cronograma Diario de Actividades'
    title = 'Cronograma Diario de Actividades'
    nombre_colaborador = vendedor.nombre_vendedor
    sucursal_colaborador = vendedor.sucursal
    fecha_actual = vendedor.dia_reporte


    canvas = Canvas(file_name, pagesize=landscape(letter))

    doc = BaseDocTemplate(file_name)
    contents =[]
    width,height = A4

    left_header_frame = Frame(
        0.2*inch, 
        height-1.2*inch, 
        2*inch, 
        1*inch
        )

    right_header_frame = Frame(
        2.2*inch, 
        height-1.2*inch, 
        width-2.5*inch, 
        1*inch,id='normal'
        )

    frame_later = Frame(
        0.2*inch, 
        0.6*inch, 
        (width-0.6*inch)+0.17*inch, 
        height-1*inch,
        leftPadding = 0, 
        topPadding=0, 
        showBoundary = 1,
        id='col'
        )

    frame_table= Frame(
        0.2*inch, 
        0.7*inch, 
        (width-0.6*inch)+0.17*inch, 
        height-2*inch,
        leftPadding = 0, 
        topPadding=0, 
        showBoundary = 1,
        id='col'
        )
    laterpages = PageTemplate(id='laterpages',frames=[frame_later])

    firstpage = PageTemplate(id='firstpage',frames=[left_header_frame, right_header_frame,frame_table],)

    contents.append(NextPageTemplate('firstpage'))
    #logoleft = Image('logo_power.png')
    #logoleft._restrictSize(1.5*inch, 1.5*inch)
    #logoleft.hAlign = 'CENTER'
    #logoleft.vAlign = 'CENTER'

    #contents.append(logoleft)
    contents.append(FrameBreak())
    styleSheet = getSampleStyleSheet()
    style_title = styleSheet['Heading1']
    style_title.fontSize = 20 
    style_title.fontName = 'Helvetica-Bold'
    style_title.alignment=TA_CENTER

    style_data = styleSheet['Normal']
    style_data.fontSize = 16 
    style_data.fontName = 'Helvetica'
    style_data.alignment=TA_CENTER

    style_date = styleSheet['Normal']
    style_date.fontSize = 14
    style_date.fontName = 'Helvetica'
    style_date.alignment=TA_CENTER

    canvas.setTitle(document_title)

    contents.append(Paragraph(title, style_title))
    contents.append(Paragraph(nombre_colaborador + ' - ' + sucursal_colaborador, style_data))
    contents.append(Paragraph(fecha_actual, style_date))
    contents.append(FrameBreak())

    title_background = colors.fidblue
    hour = 8
    minute = 0
    hour_list = []

    data_actividades = [
        {'Hora', 'Cliente', 'Resultado de \nActividad', 'Monto Venta \n(MXN)', 'Monto Venta \n(USD)',
        'Monto Cotización \n(MXN)', 'Monto Cotización \n(USD)', 'Comentarios \nAdicionales'},
    ]

    i = 0
    for i in range(300):

        if minute == 0:
            if hour <= 12:
                time = str(hour) + ':' + str(minute) + '0 a.m.'
            else:
                time = str(hour-12) + ':' + str(minute) + '0 p.m.'
        else:
            if hour <= 12:
                time = str(hour) + ':' + str(minute) + ' a.m.'
            else:
                time = str(hour-12) + ':' + str(minute) + ' p.m.'

        if minute != 45:
            minute += 15
        else:
            hour += 1
            minute = 0
        hour_list.append(time)

        # I TRIED THIS SOLUTION BUT THIS DIDN'T WORK
        # if i % 20 == 0:
        

        data_actividades.append([hour_list[i], i, i, i, i, i, i, i])

        i += 1

        table_actividades = Table(data_actividades, colWidths=85, rowHeights=30, repeatRows=1)
        tblStyle = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), title_background),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        rowNumb = len(data_actividades)
        for row in range(1, rowNumb):
            if row % 2 == 0:
                table_background = colors.lightblue
            else:
                table_background = colors.aliceblue

            tblStyle.add('BACKGROUND', (0, row), (-1, row), table_background)

        table_actividades.setStyle(tblStyle)

        width = 150
        height = 150
        
    contents.append(NextPageTemplate('laterpages'))
    contents.append(table_actividades)


    contents.append(PageBreak())


    doc.addPageTemplates([firstpage,laterpages])
    doc.build(contents)

    response = HttpResponse(mimetype='application/pdf')
    response.write(doc)
    response['Content-Disposition'] = 'attachment; filename=output.pdf'

    return response