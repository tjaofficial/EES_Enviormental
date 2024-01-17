from django.shortcuts import HttpResponse
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from .print_form_view import PageNumCanvas
from django.http import HttpResponseNotFound
import io
import datetime
from .form_pdf_templates import pdf_template_invoice
from ..utils import braintreeGateway
from ..models import user_profile_model


def invoices(request, invoiceID):
    userProf = user_profile_model.objects.get(user__id=request.user.id)
    gateway = braintreeGateway()
    transactionData = gateway.transaction.find(invoiceID)
    documentTitle = 'MP_INVOICE_'+invoiceID
    title = 'Tax Invoice'
    marginSet = 0.4
    stream = io.BytesIO()
    tableData, tableColWidths, style = pdf_template_invoice(transactionData, userProf, title)
    pdf = SimpleDocTemplate(stream, pagesize=letter, topMargin=marginSet*inch, bottomMargin=0.3*inch, title=documentTitle)
    table = Table(tableData, colWidths=tableColWidths)
    style = TableStyle(style)
    table.setStyle(style)
    try:
        pdf.build([table], canvasmaker=PageNumCanvas)
        stream.seek(0)
        pdf_buffer = stream.getbuffer()
        print(pdf_buffer)
        response = HttpResponse(bytes(pdf_buffer), content_type='application/pdf')
    except UnboundLocalError as e:
        return HttpResponseNotFound("No Forms Found")
    
    
    return response