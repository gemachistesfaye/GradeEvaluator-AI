import csv
from io import StringIO
from flask import Response

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
