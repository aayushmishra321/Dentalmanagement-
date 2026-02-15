"""
Report Generation Utilities for Phase 5
Automated report generation with PDF, CSV, and Excel support
"""

import os
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models import Count, Sum, Avg, Q
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
import csv
from io import BytesIO, StringIO

from home.models import (
    UserDetail, DoctorDetail, bookappointment, appointmenthistory,
    Payment, DoctorRating, MedicalRecord, Report
)


# ============================================================================
# REPORT GENERATION FUNCTIONS
# ============================================================================

def generate_daily_appointments_report(date=None):
    """Generate daily appointments report"""
    if not date:
        date = datetime.now().date()
    
    appointments = bookappointment.objects.filter(appdate=str(date))
    
    data = {
        'date': date,
        'total_appointments': appointments.count(),
        'appointments': list(appointments.values(
            'username', 'doctorname', 'apptime', 'clinicname', 'consultationfee'
        )),
        'total_revenue': sum([float(a.consultationfee.replace('₹', '').replace('+', '').strip()) 
                             for a in appointments if a.consultationfee])
    }
    
    return data


def generate_monthly_revenue_report(year=None, month=None):
    """Generate monthly revenue report"""
    if not year:
        year = datetime.now().year
    if not month:
        month = datetime.now().month
    
    # Get completed payments for the month
    payments = Payment.objects.filter(
        payment_status='completed',
        payment_date__year=year,
        payment_date__month=month
    )
    
    data = {
        'year': year,
        'month': month,
        'total_revenue': payments.aggregate(total=Sum('amount'))['total'] or 0,
        'total_transactions': payments.count(),
        'payment_methods': payments.values('payment_method').annotate(
            count=Count('id'),
            total=Sum('amount')
        ),
        'top_doctors': payments.values('doctor__name').annotate(
            revenue=Sum('amount')
        ).order_by('-revenue')[:10]
    }
    
    return data


def generate_patient_statistics_report():
    """Generate patient statistics report"""
    total_patients = UserDetail.objects.count()
    
    # Gender distribution
    gender_dist = UserDetail.objects.values('gender').annotate(count=Count('email'))
    
    # Active patients (had appointment in last 30 days)
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    active_patients = bookappointment.objects.filter(
        appdate__gte=thirty_days_ago
    ).values('useremail').distinct().count()
    
    # New patients this month - simplified query
    current_month = datetime.now().strftime('%Y-%m')
    new_patients_this_month = bookappointment.objects.filter(
        appdate__startswith=current_month
    ).values('useremail').distinct().count()
    
    data = {
        'total_patients': total_patients,
        'active_patients': active_patients,
        'gender_distribution': list(gender_dist),
        'new_patients_this_month': new_patients_this_month
    }
    
    return data


def generate_doctor_performance_report():
    """Generate doctor performance report"""
    doctors = DoctorDetail.objects.all()
    
    performance_data = []
    for doctor in doctors:
        # Get appointments
        total_appointments = appointmenthistory.objects.filter(doctoremail=doctor.email).count()
        
        # Get revenue
        total_revenue = Payment.objects.filter(
            doctor=doctor,
            payment_status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Get ratings
        avg_rating = DoctorRating.objects.filter(
            doctor=doctor,
            is_verified=True
        ).aggregate(avg=Avg('rating'))['avg'] or 0
        
        performance_data.append({
            'doctor_name': doctor.name,
            'total_appointments': total_appointments,
            'total_revenue': float(total_revenue),
            'average_rating': round(float(avg_rating), 2),
            'clinic': doctor.clinicname,
            'city': doctor.city
        })
    
    # Sort by revenue
    performance_data.sort(key=lambda x: x['total_revenue'], reverse=True)
    
    return {'doctors': performance_data}


# ============================================================================
# PDF GENERATION
# ============================================================================

def generate_pdf_report(report_data, report_type, filename):
    """Generate PDF report"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph(f"<b>{report_type.replace('_', ' ').title()} Report</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Date
    date_text = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
    elements.append(date_text)
    elements.append(Spacer(1, 0.2*inch))
    
    # Content based on report type
    if report_type == 'daily_appointments':
        # Summary
        summary = Paragraph(f"<b>Total Appointments:</b> {report_data['total_appointments']}<br/>"
                          f"<b>Total Revenue:</b> ₹{report_data['total_revenue']:.2f}", styles['Normal'])
        elements.append(summary)
        elements.append(Spacer(1, 0.2*inch))
        
        # Table
        if report_data['appointments']:
            table_data = [['Patient', 'Doctor', 'Time', 'Clinic', 'Fee']]
            for apt in report_data['appointments']:
                table_data.append([
                    apt['username'],
                    apt['doctorname'],
                    apt['apptime'],
                    apt['clinicname'][:20],
                    apt['consultationfee']
                ])
            
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
    
    elif report_type == 'monthly_revenue':
        # Summary
        summary = Paragraph(f"<b>Month:</b> {report_data['month']}/{report_data['year']}<br/>"
                          f"<b>Total Revenue:</b> ₹{report_data['total_revenue']:.2f}<br/>"
                          f"<b>Total Transactions:</b> {report_data['total_transactions']}", styles['Normal'])
        elements.append(summary)
    
    # Build PDF
    doc.build(elements)
    
    # Save to file
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'reports', filename)
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    
    with open(pdf_path, 'wb') as f:
        f.write(buffer.getvalue())
    
    return pdf_path


# ============================================================================
# CSV GENERATION
# ============================================================================

def generate_csv_report(report_data, report_type, filename):
    """Generate CSV report"""
    csv_path = os.path.join(settings.MEDIA_ROOT, 'reports', filename)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        if report_type == 'daily_appointments':
            fieldnames = ['Patient', 'Doctor', 'Time', 'Clinic', 'Fee']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for apt in report_data['appointments']:
                writer.writerow({
                    'Patient': apt['username'],
                    'Doctor': apt['doctorname'],
                    'Time': apt['apptime'],
                    'Clinic': apt['clinicname'],
                    'Fee': apt['consultationfee']
                })
        
        elif report_type == 'doctor_performance':
            fieldnames = ['Doctor', 'Appointments', 'Revenue', 'Rating', 'Clinic', 'City']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for doc in report_data['doctors']:
                writer.writerow({
                    'Doctor': doc['doctor_name'],
                    'Appointments': doc['total_appointments'],
                    'Revenue': doc['total_revenue'],
                    'Rating': doc['average_rating'],
                    'Clinic': doc['clinic'],
                    'City': doc['city']
                })
    
    return csv_path


# ============================================================================
# MAIN REPORT GENERATION
# ============================================================================

def generate_report(report_type, file_format='pdf', start_date=None, end_date=None):
    """Main report generation function"""
    try:
        # Generate report data
        if report_type == 'daily_appointments':
            report_data = generate_daily_appointments_report(start_date)
        elif report_type == 'monthly_revenue':
            year = start_date.year if start_date else None
            month = start_date.month if start_date else None
            report_data = generate_monthly_revenue_report(year, month)
        elif report_type == 'patient_statistics':
            report_data = generate_patient_statistics_report()
        elif report_type == 'doctor_performance':
            report_data = generate_doctor_performance_report()
        else:
            raise ValueError(f"Unknown report type: {report_type}")
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{report_type}_{timestamp}.{file_format}"
        
        # Generate file
        if file_format == 'pdf':
            file_path = generate_pdf_report(report_data, report_type, filename)
        elif file_format == 'csv':
            file_path = generate_csv_report(report_data, report_type, filename)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")
        
        return file_path, report_data
        
    except Exception as e:
        raise Exception(f"Report generation failed: {str(e)}")
