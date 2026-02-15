"""
Celery Tasks for Dental Management System
Background tasks for appointment reminders, reports, and notifications
"""

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from home.models import bookappointment, DoctorDetail, UserDetail
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_appointment_reminders():
    """
    Send email reminders for appointments happening in the next 24 hours
    Runs every hour via Celery Beat
    """
    try:
        # Get tomorrow's date
        tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Get all appointments for tomorrow
        appointments = bookappointment.objects.filter(appdate=tomorrow)
        
        sent_count = 0
        for appointment in appointments:
            try:
                # Send reminder email to patient
                send_mail(
                    subject="Appointment Reminder - Tomorrow",
                    message=f"""
                    Hi {appointment.username},
                    
                    This is a reminder that you have an appointment tomorrow:
                    
                    Date: {appointment.appdate}
                    Time: {appointment.apptime}
                    Doctor: Dr. {appointment.doctorname}
                    Clinic: {appointment.clinicname}, {appointment.city}
                    Consultation Fee: ₹{appointment.consultationfee}
                    
                    Please arrive 10 minutes early.
                    
                    If you need to reschedule, please contact us as soon as possible.
                    
                    Thank you,
                    Dental Management Team
                    """,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[appointment.useremail],
                    fail_silently=True,
                )
                sent_count += 1
                logger.info(f"Reminder sent to {appointment.useremail} for appointment on {appointment.appdate}")
            except Exception as e:
                logger.error(f"Failed to send reminder to {appointment.useremail}: {str(e)}")
        
        logger.info(f"Sent {sent_count} appointment reminders")
        return f"Sent {sent_count} reminders"
        
    except Exception as e:
        logger.error(f"Error in send_appointment_reminders: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def send_appointment_reminder_24hrs(appointment_id):
    """
    Send 24-hour reminder for a specific appointment
    Called when appointment is booked
    """
    try:
        appointment = bookappointment.objects.get(id=appointment_id)
        
        send_mail(
            subject="Appointment Reminder - 24 Hours",
            message=f"""
            Hi {appointment.username},
            
            Your appointment is in 24 hours:
            
            Date: {appointment.appdate}
            Time: {appointment.apptime}
            Doctor: Dr. {appointment.doctorname}
            Clinic: {appointment.clinicname}, {appointment.city}
            
            See you soon!
            
            Dental Management Team
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[appointment.useremail],
            fail_silently=True,
        )
        
        logger.info(f"24hr reminder sent for appointment {appointment_id}")
        return "Reminder sent"
        
    except Exception as e:
        logger.error(f"Failed to send 24hr reminder: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def cleanup_old_sessions():
    """
    Clean up expired sessions from database
    Runs daily at 2 AM
    """
    try:
        from django.core.management import call_command
        call_command('clearsessions')
        logger.info("Old sessions cleaned up")
        return "Sessions cleaned"
    except Exception as e:
        logger.error(f"Error cleaning sessions: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def generate_daily_reports():
    """
    Generate and send daily reports to doctors
    Runs daily at 8 AM
    """
    try:
        today = datetime.today().strftime('%Y-%m-%d')
        doctors = DoctorDetail.objects.all()
        
        sent_count = 0
        for doctor in doctors:
            # Get today's appointments for this doctor
            appointments = bookappointment.objects.filter(
                doctoremail=doctor.email,
                appdate=today
            )
            
            if appointments.exists():
                # Create report
                report = f"""
                Daily Schedule Report - {today}
                
                Dr. {doctor.name}
                {doctor.clinicname}, {doctor.city}
                
                Today's Appointments: {appointments.count()}
                
                Schedule:
                """
                
                for apt in appointments:
                    report += f"\n{apt.apptime} - {apt.username} ({apt.useremail})"
                
                report += "\n\nHave a great day!\n\nDental Management System"
                
                # Send email
                try:
                    send_mail(
                        subject=f"Daily Schedule - {today}",
                        message=report,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[doctor.email],
                        fail_silently=True,
                    )
                    sent_count += 1
                    logger.info(f"Daily report sent to Dr. {doctor.name}")
                except Exception as e:
                    logger.error(f"Failed to send report to {doctor.email}: {str(e)}")
        
        logger.info(f"Sent {sent_count} daily reports")
        return f"Sent {sent_count} reports"
        
    except Exception as e:
        logger.error(f"Error generating daily reports: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def send_welcome_email(user_email, user_name):
    """
    Send welcome email to new users
    Called asynchronously after registration
    """
    try:
        send_mail(
            subject="Welcome to Dental Management System",
            message=f"""
            Hi {user_name},
            
            Welcome to Dental Management System!
            
            Thank you for registering with us. We're excited to help you maintain your dental health.
            
            You can now:
            - Book appointments with top dentists
            - View your appointment history
            - Manage your profile
            - Receive appointment reminders
            
            If you have any questions, feel free to contact us.
            
            Best regards,
            Dental Management Team
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            fail_silently=True,
        )
        
        logger.info(f"Welcome email sent to {user_email}")
        return "Welcome email sent"
        
    except Exception as e:
        logger.error(f"Failed to send welcome email: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def send_birthday_wishes():
    """
    Send birthday wishes to users
    Runs daily to check for birthdays
    """
    try:
        today = datetime.today()
        today_str = today.strftime('%m-%d')  # MM-DD format
        
        # Get all users with birthday today
        users = UserDetail.objects.all()
        sent_count = 0
        
        for user in users:
            try:
                # Extract month and day from dateofbirth
                if user.dateofbirth:
                    dob_parts = user.dateofbirth.split('-')
                    if len(dob_parts) >= 2:
                        user_birthday = f"{dob_parts[1]}-{dob_parts[2]}"
                        
                        if user_birthday == today_str:
                            send_mail(
                                subject="Happy Birthday! 🎉",
                                message=f"""
                                Happy Birthday, {user.name}! 🎂
                                
                                Wishing you a wonderful day filled with joy and happiness!
                                
                                As a birthday gift, enjoy 10% off on your next appointment.
                                
                                Best wishes,
                                Dental Management Team
                                """,
                                from_email=settings.EMAIL_HOST_USER,
                                recipient_list=[user.email],
                                fail_silently=True,
                            )
                            sent_count += 1
                            logger.info(f"Birthday wishes sent to {user.email}")
            except Exception as e:
                logger.error(f"Error sending birthday wish to {user.email}: {str(e)}")
        
        logger.info(f"Sent {sent_count} birthday wishes")
        return f"Sent {sent_count} birthday wishes"
        
    except Exception as e:
        logger.error(f"Error in send_birthday_wishes: {str(e)}")
        return f"Error: {str(e)}"
