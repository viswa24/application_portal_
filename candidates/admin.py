from django.contrib import admin
from .models import Candidate, EducationQualification, WorkExperience
from django.http import HttpResponse
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import io

class EducationQualificationInline(admin.TabularInline):
    model = EducationQualification
    extra = 1

class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 1

def format_education(candidate):
    edus = candidate.education_qualifications.all()
    return ' | '.join([
        f"{e.course}, {e.specialisation}, {e.board_institute}, {e.month_of_completion}/{e.year_of_completion}, {e.percentage}%, {e.class_obtained}" for e in edus
    ])

def format_work(candidate):
    works = candidate.work_experiences.all()
    return ' | '.join([
        f"{w.institution}, {w.designation}, {w.from_date} to {w.to_date}, {w.tasks_duties}" for w in works
    ])

def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=candidates.csv'
    writer = csv.writer(response)
    writer.writerow([
        'Application Number', 'Name', 'Post', 'Date of Birth', 'Email', 'Phone', 'Caste', 'Religion', 'Category',
        'Permanent Address', 'Communication Address', 'Same as Permanent',
        'Experience Match', 'Photo', 'Signature', 'Created At', 'Updated At',
        'Education Qualifications', 'Work Experience'
    ])
    for obj in queryset:
        writer.writerow([
            obj.id, obj.name, obj.post, obj.date_of_birth, obj.email, obj.phone, obj.caste, obj.religion, obj.category,
            f"{obj.permanent_line1}, {obj.permanent_line2}, {obj.permanent_city}, {obj.permanent_district}, {obj.permanent_state}, {obj.permanent_pincode}",
            f"{obj.communication_line1}, {obj.communication_line2}, {obj.communication_city}, {obj.communication_district}, {obj.communication_state}, {obj.communication_pincode}",
            obj.same_as_permanent,
            obj.experience_match,
            obj.photo.url if obj.photo else '',
            obj.signature.url if obj.signature else '',
            obj.created_at,
            obj.updated_at,
            format_education(obj),
            format_work(obj)
        ])
    return response
export_as_csv.short_description = "Export Selected as CSV"

def export_as_pdf(modeladmin, request, queryset):
    buffer = io.BytesIO()
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    for obj in queryset:
        data = [
            ['Application Number', obj.id],
            ['Name', obj.name],
            ['Post', obj.post],
            ['Date of Birth', str(obj.date_of_birth)],
            ['Email', obj.email],
            ['Phone', obj.phone],
            ['Caste', obj.caste],
            ['Religion', obj.religion],
            ['Category', obj.category],
            ['Permanent Address', f"{obj.permanent_line1}, {obj.permanent_line2}, {obj.permanent_city}, {obj.permanent_district}, {obj.permanent_state}, {obj.permanent_pincode}"],
            ['Communication Address', f"{obj.communication_line1}, {obj.communication_line2}, {obj.communication_city}, {obj.communication_district}, {obj.communication_state}, {obj.communication_pincode}"],
            ['Same as Permanent', str(obj.same_as_permanent)],
            ['Experience Match', obj.experience_match],
            ['Photo', obj.photo.url if obj.photo else ''],
            ['Signature', obj.signature.url if obj.signature else ''],
            ['Created At', str(obj.created_at)],
            ['Updated At', str(obj.updated_at)],
        ]
        table = Table(data, colWidths=[150, 350])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))
        # Education Qualifications Table
        edus = obj.education_qualifications.all()
        if edus:
            edu_data = [['Course', 'Specialisation', 'Board/Institute', 'Month', 'Year', 'Percentage', 'Class']]
            for e in edus:
                edu_data.append([
                    e.course, e.specialisation, e.board_institute, e.month_of_completion, e.year_of_completion, str(e.percentage), e.class_obtained
                ])
            edu_table = Table(edu_data, colWidths=[70, 70, 70, 40, 40, 40, 40])
            edu_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(Paragraph('Education Qualifications:', styles['Heading4']))
            elements.append(edu_table)
            elements.append(Spacer(1, 12))
        # Work Experience Table
        works = obj.work_experiences.all()
        if works:
            work_data = [['Institution', 'Designation', 'From', 'To', 'Tasks/Duties']]
            for w in works:
                work_data.append([
                    w.institution, w.designation, str(w.from_date), str(w.to_date), w.tasks_duties
                ])
            work_table = Table(work_data, colWidths=[70, 70, 50, 50, 100])
            work_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(Paragraph('Work Experience:', styles['Heading4']))
            elements.append(work_table)
            elements.append(Spacer(1, 12))
        elements.append(Spacer(1, 24))
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=candidates.pdf'
    response.write(pdf)
    return response
export_as_pdf.short_description = "Export Each Candidate as PDF (Table per Page)"

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'post', 'email', 'category', 'created_at')
    search_fields = ('name', 'post', 'category', 'email')
    actions = [export_as_csv, export_as_pdf]
    inlines = [EducationQualificationInline, WorkExperienceInline]
