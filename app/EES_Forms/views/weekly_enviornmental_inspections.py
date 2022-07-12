from fpdf import FPDF
from ..models import formA1_model

selected_form = formA1_model.objects.all().order_by('-date')

pdf = FPDF('P', 'in', 'Letter')
pdf.add_page()
pdf.set_font('Arial', size = 10)


pdf.cell(.75,.20, txt = 'Facility Name:', ln = 6, align = "L")
pdf.cell(.75,.20, txt = 'Inspectors Name:', ln = 7, align = "L")
#pdf.cell(200,10, txt = 'Method 303 Charging', ln = 1, align = "C")
#pdf.cell(200,10, txt = 'Certification Form', ln = 2, align = "C")
#pdf.cell(200,10, txt = 'Form A-1', ln = 3, align = "C")

#saving the PDF
pdf.output("test_pdf.pdf")