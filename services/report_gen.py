from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.units import inch
import os
from datetime import datetime

def generate_pdf(report_data):
    
    report_dir = os.path.join("static", "reports")
    os.makedirs(report_dir, exist_ok=True)
    
 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"SAKHI_Report_{report_data['incident_id']}_{timestamp}.pdf"
    pdf_path = os.path.join(report_dir, filename)
    
  
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        textColor=HexColor('#3E096B'), 
        spaceAfter=30,
        fontSize=24,
        alignment=1  
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        textColor=HexColor('#3E096B'),
        fontSize=14,
        spaceBefore=15,
        spaceAfter=5
    )
    
    content_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceBefore=5,
        spaceAfter=15
    )
    

    story = []

    story.append(Paragraph("SAKHI - Incident Report", title_style))
    story.append(Spacer(1, 20))

    details = [
        ('Report ID', report_data['incident_id']),
        ('Date & Time', report_data['date_time'].strftime("%Y-%m-%d %H:%M")),
        ('Location', report_data['location']),
        ('Incident Type', report_data['incident_type']),
        ('Severity Level', report_data['severity'])
    ]
    
    for label, value in details:
        story.append(Paragraph(f"<b>{label}:</b> {value}", content_style))
    
    story.append(Paragraph("Incident Description", heading_style))
    story.append(Paragraph(report_data['description'], content_style))
    

    story.append(Spacer(1, 30))
    story.append(Paragraph(
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=HexColor('#666666'))
    ))
    
    doc.build(story)
    
    return {
        'filename': filename,
        'filepath': pdf_path,
        'download_url': f"/report/download/{filename}"
    }