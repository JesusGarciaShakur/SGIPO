from flask import Blueprint, jsonify, render_template, redirect, request, session, abort, url_for
import io
import pdfkit
from flask import render_template, request, send_file
import io
from models.sales import generate_report
from flask import Response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
from models.db import get_connection

mydb = get_connection()

report_views = Blueprint('report', __name__)

@report_views.route('/sales_report', methods=['GET'])
def sales_report():
    if session.get('user') and session.get('user')['type'] == 1:
        # Obtener parámetros de fechas
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

        # Consultar las ventas en el rango de fechas
        sales = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = """
                SELECT * FROM vista_ventas
                WHERE `fecha de venta` BETWEEN %s AND %s
                ORDER BY `fecha de venta`
            """
            cursor.execute(sql, (start_date, end_date))
            sales = cursor.fetchall()

        if not sales:
            return jsonify({'message': 'No sales found in the specified date range.'}), 404

        # Verificar los datos retornados
        print("Sales data:", sales)

        # Calcular el total de ventas
        total_sales = sum(sale['precio final'] for sale in sales)

        # Crear el PDF
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setTitle("Sales Report")

        # Configuración del encabezado
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200, 750, "Sales Report")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, 730, f"From: {start_date.strftime('%Y-%m-%d')} To: {end_date.strftime('%Y-%m-%d')}")
        pdf.drawString(50, 710, f"Total Sales: ${total_sales:.2f}")  # Mostrar el total de ventas

        # Columnas
        y = 680
        pdf.drawString(50, y, "ID Sale")
        pdf.drawString(100, y, "Client")
        pdf.drawString(200, y, "Product")
        pdf.drawString(300, y, "Quantity")
        pdf.drawString(400, y, "Final Price")
        pdf.drawString(500, y, "Date Sold")
        y -= 20

        # Datos
        pdf.setFont("Helvetica", 10)
        for sale in sales:
            pdf.drawString(50, y, str(sale['id de venta']))
            pdf.drawString(100, y, sale['nombre cliente'])
            pdf.drawString(200, y, sale['nombre producto'])
            pdf.drawString(300, y, str(sale['articulos vendidos']))
            pdf.drawString(400, y, f"${sale['precio final']:.2f}")
            pdf.drawString(500, y, sale['fecha venta'].strftime('%Y-%m-%d'))
            y -= 20
            if y < 50:  # Nueva página si es necesario
                pdf.showPage()
                y = 750

        pdf.save()
        buffer.seek(0)

        # Enviar el archivo PDF como respuesta
        return Response(buffer, mimetype='application/pdf', headers={
            'Content-Disposition': f'attachment;filename=Sales_Report_{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}.pdf'
        })
    else:
        abort(403)

@report_views.route('/generate_report', methods=['GET'])
def generate_report_view():
    if session.get('user') and session.get('user')['type'] == 1:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date and end_date:
            sales = generate_report(start_date, end_date)
        else:
            sales = []

        return render_template('pages/report/report.html', sales=sales)
    else:
        abort(403)

@report_views.route('/generate_pdf', methods=['GET'])
def generate_pdf():
    if session.get('user') and session.get('user')['type'] == 1:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'Debe proporcionar las fechas de inicio y fin.'}), 400

        # Obtener las ventas desde la base de datos
        sales = generate_report(start_date, end_date)  # Función para obtener los datos de ventas
        
        # Calcular el total de ventas
        total_sales = sum(sale['precio final'] for sale in sales) if sales else 0

        # Renderizar el HTML con los datos
        rendered = render_template(
            'pages/report/sale_report.html',
            sales=sales,
            start_date=start_date,
            end_date=end_date,
            total_sales=total_sales
        )
        
        # Configurar pdfkit con la ruta de wkhtmltopdf
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        
        # Convertir el HTML a PDF
        pdf = pdfkit.from_string(rendered, False, configuration=config)
        
        # Enviar el PDF como archivo descargable
        return send_file(io.BytesIO(pdf), as_attachment=True, download_name="reporte_ventas.pdf", mimetype='application/pdf')
    else:
        abort(403)