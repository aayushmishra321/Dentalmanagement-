"""
Utility functions for Dental Management System
Helper functions for PDF generation, notifications, etc.
"""

from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def generate_invoice_pdf(payment):
    """
    Generate PDF invoice for a payment
    Returns BytesIO buffer with PDF content
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=12
    )
    
    # Title
    title = Paragraph("INVOICE", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Invoice details
    invoice_data = [
        ['Invoice Number:', payment.invoice_number],
        ['Date:', payment.payment_date.strftime('%B %d, %Y')],
        ['Payment Status:', payment.payment_status.upper()],
    ]
    
    invoice_table = Table(invoice_data, colWidths=[2*inch, 3*inch])
    invoice_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(invoice_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Bill To section
    bill_to = Paragraph("Bill To:", heading_style)
    elements.append(bill_to)
    
    patient_data = [
        ['Patient Name:', payment.patient.name],
        ['Email:', payment.patient.email],
        ['Contact:', payment.patient.contact],
        ['Address:', payment.patient.address],
    ]
    
    patient_table = Table(patient_data, colWidths=[2*inch, 3*inch])
    patient_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(patient_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Service Provider section
    provider = Paragraph("Service Provider:", heading_style)
    elements.append(provider)
    
    doctor_data = [
        ['Doctor Name:', f"Dr. {payment.doctor.name}"],
        ['Clinic:', payment.doctor.clinicname],
        ['Location:', payment.doctor.city],
        ['Contact:', payment.doctor.contact],
    ]
    
    doctor_table = Table(doctor_data, colWidths=[2*inch, 3*inch])
    doctor_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(doctor_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Services table
    services_heading = Paragraph("Services:", heading_style)
    elements.append(services_heading)
    
    service_data = [
        ['Description', 'Amount'],
        ['Dental Consultation', f"₹{payment.amount}"],
    ]
    
    service_table = Table(service_data, colWidths=[4*inch, 1.5*inch])
    service_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(service_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Total
    total_data = [
        ['Total Amount:', f"₹{payment.amount}"],
        ['Payment Method:', payment.payment_method.upper()],
    ]
    
    total_table = Table(total_data, colWidths=[4*inch, 1.5*inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.black),
    ]))
    elements.append(total_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    footer = Paragraph("Thank you for choosing our dental services!", footer_style)
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


def send_invoice_email(payment):
    """
    Generate and send invoice via email
    """
    try:
        # Generate PDF
        pdf_buffer = generate_invoice_pdf(payment)
        
        # Create email
        subject = f"Invoice {payment.invoice_number} - Dental Management"
        message = f"""
        Dear {payment.patient.name},
        
        Thank you for your payment. Please find attached your invoice.
        
        Invoice Number: {payment.invoice_number}
        Amount: ₹{payment.amount}
        Payment Date: {payment.payment_date.strftime('%B %d, %Y')}
        Payment Status: {payment.payment_status.upper()}
        
        If you have any questions, please don't hesitate to contact us.
        
        Best regards,
        Dental Management Team
        """
        
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[payment.patient.email],
        )
        
        # Attach PDF
        email.attach(
            f'invoice_{payment.invoice_number}.pdf',
            pdf_buffer.getvalue(),
            'application/pdf'
        )
        
        email.send(fail_silently=True)
        logger.info(f"Invoice sent to {payment.patient.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send invoice: {str(e)}")
        return False


def calculate_doctor_average_rating(doctor):
    """
    Calculate average rating for a doctor
    """
    from home.models import DoctorRating
    ratings = DoctorRating.objects.filter(doctor=doctor, is_verified=True)
    
    if ratings.exists():
        total = sum(r.rating for r in ratings)
        return round(total / ratings.count(), 1)
    return 0


def create_notification(user=None, doctor=None, title="", message="", notification_type="system"):
    """
    Create a notification for user or doctor
    """
    from home.models import Notification
    
    try:
        notification = Notification.objects.create(
            user=user,
            doctor=doctor,
            title=title,
            message=message,
            notification_type=notification_type
        )
        logger.info(f"Notification created: {title}")
        return notification
    except Exception as e:
        logger.error(f"Failed to create notification: {str(e)}")
        return None


def get_unread_notifications_count(user=None, doctor=None):
    """
    Get count of unread notifications
    """
    from home.models import Notification
    
    if user:
        return Notification.objects.filter(user=user, is_read=False).count()
    elif doctor:
        return Notification.objects.filter(doctor=doctor, is_read=False).count()
    return 0


def mark_notification_as_read(notification_id):
    """
    Mark a notification as read
    """
    from home.models import Notification
    
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return True
    except Exception as e:
        logger.error(f"Failed to mark notification as read: {str(e)}")
        return False
