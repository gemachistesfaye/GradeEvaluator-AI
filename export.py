import csv
import datetime
from io import StringIO, BytesIO
from flask import Response
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def export_grades_csv(grades):
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Date', 'Subject', 'Score', 'Letter Grade', 'GPA Points'])
    for row in grades:
        cw.writerow([row['date'], row['subject'], row['score'], row['letter_grade'], row['gpa_points']])
    
    return Response(
        si.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=grades_history.csv"}
    )

def export_grades_pdf(grades, student_name):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    elements.append(Paragraph("GradeEvaluator — Grade Report", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Student Name: {student_name}", styles['Normal']))
    date_str = datetime.datetime.now().strftime("%B %d, %Y")
    elements.append(Paragraph(f"Export Date: {date_str}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    data = [['Date', 'Subject', 'Score', 'Letter Grade', 'GPA']]
    total_score = 0
    total_gpa = 0
    
    for row in grades:
        data.append([row['date'], row['subject'], str(row['score']), row['letter_grade'], str(row['gpa_points'])])
        total_score += row['score']
        total_gpa += row['gpa_points']
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))
    
    if len(grades) > 0:
        avg_score = total_score / len(grades)
        avg_gpa = total_gpa / len(grades)
        elements.append(Paragraph(f"Total grades: {len(grades)}", styles['Normal']))
        elements.append(Paragraph(f"Average score: {avg_score:.2f}", styles['Normal']))
        elements.append(Paragraph(f"Average GPA: {avg_gpa:.2f}", styles['Normal']))
    
    doc.build(elements)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-disposition": "attachment; filename=grades_report.pdf"}
    )
