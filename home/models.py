
from django.db import models

# Create your models here.


#for patient user models

# registration model
class UserDetail(models.Model):
    name=models.CharField(max_length=200 )
    email=models.EmailField(max_length=200,primary_key=True)
    contact=models.CharField(max_length=12, unique=True,null=False)
    dateofbirth=models.CharField(max_length=200,null=False)
    gender=models.CharField( max_length=50,null=False)
    address=models.TextField(null=False)
    pincode=models.CharField(max_length=10,null=False)
    password=models.CharField(max_length=100,null=False)



# for user contact
class UserContacts(models.Model):
    name=models.CharField(max_length=200 )
    email=models.EmailField(max_length=200)
    contact=models.CharField(max_length=12)
    message=models.TextField(null=False)
    date=models.DateField()


# for doctor contact
class DoctorsMessage(models.Model):
    name=models.CharField(max_length=200 )
    email=models.EmailField(max_length=200)
    contact=models.CharField(max_length=12)
    message=models.TextField(null=False)
    date=models.DateField()



# doctor detail
class DoctorDetail(models.Model):
    name=models.CharField(max_length=200 )
    email=models.EmailField(max_length=200,primary_key=True)
    contact=models.CharField(max_length=12, unique=True,null=False)
    experience=models.CharField(max_length=100)
    clinicname=models.TextField(null=False)
    city=models.CharField(max_length=200)
    consultationfee=models.CharField(max_length=10)
    password=models.CharField(max_length=100,null=False)

# book appointment
class bookappointment(models.Model):
    username=models.CharField(max_length=200 )
    useremail=models.EmailField(max_length=200)
    
    doctorname=models.CharField(max_length=200 )
    doctoremail=models.EmailField(max_length=200)
    clinicname=models.TextField(null=False)
    city=models.CharField(max_length=200)
    appdate=models.CharField(max_length=200)
    apptime=models.CharField(max_length=100)
    consultationfee=models.CharField(max_length=10)
    payment=models.CharField(max_length=100)


#  appointment history
class appointmenthistory(models.Model):
    username=models.CharField(max_length=200 )
    useremail=models.EmailField(max_length=200)
    
    doctorname=models.CharField(max_length=200 )
    doctoremail=models.EmailField(max_length=200)
    
    appdate=models.CharField(max_length=200)
    apptime=models.CharField(max_length=100)
    consultationfee=models.CharField(max_length=100)
    payment=models.CharField(max_length=100)
    prescription=models.TextField(max_length=1000)
    



# ============================================================================
# ADVANCED FEATURES MODELS (All Free/Open Source)
# ============================================================================

# Doctor Rating and Review System
class DoctorRating(models.Model):
    doctor = models.ForeignKey(DoctorDetail, on_delete=models.CASCADE, related_name='ratings')
    patient = models.ForeignKey(UserDetail, on_delete=models.CASCADE, related_name='given_ratings')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)  # Only patients who had appointments
    
    class Meta:
        unique_together = ('doctor', 'patient')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.patient.name} rated Dr. {self.doctor.name} - {self.rating} stars"


# Medical Records and Patient History
class MedicalRecord(models.Model):
    patient = models.ForeignKey(UserDetail, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(DoctorDetail, on_delete=models.CASCADE, related_name='created_records')
    appointment = models.ForeignKey(appointmenthistory, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Medical Information
    diagnosis = models.TextField()
    treatment_provided = models.TextField()
    medications = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Dental Specific
    teeth_treated = models.CharField(max_length=200, blank=True, null=True)  # e.g., "Upper left molar"
    procedure_type = models.CharField(max_length=200, blank=True, null=True)  # e.g., "Root Canal", "Filling"
    
    # Follow-up
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Medical Record - {self.patient.name} - {self.created_at.strftime('%Y-%m-%d')}"


# Medical Images (X-rays, Scans, etc.)
class MedicalImage(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='medical_images/%Y/%m/%d/')
    image_type = models.CharField(max_length=100, choices=[
        ('xray', 'X-Ray'),
        ('scan', 'CT Scan'),
        ('photo', 'Clinical Photo'),
        ('other', 'Other')
    ])
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.image_type} - {self.medical_record.patient.name}"


# Patient Allergies and Medical Conditions
class PatientAllergy(models.Model):
    patient = models.ForeignKey(UserDetail, on_delete=models.CASCADE, related_name='allergies')
    allergy_name = models.CharField(max_length=200)
    severity = models.CharField(max_length=50, choices=[
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe')
    ])
    notes = models.TextField(blank=True, null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Patient Allergies'
    
    def __str__(self):
        return f"{self.patient.name} - {self.allergy_name}"


# Payment Records
class Payment(models.Model):
    appointment = models.ForeignKey(bookappointment, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    patient = models.ForeignKey(UserDetail, on_delete=models.CASCADE, related_name='payments')
    doctor = models.ForeignKey(DoctorDetail, on_delete=models.CASCADE, related_name='received_payments')
    
    # Payment Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
        ('online', 'Online Banking'),
        ('insurance', 'Insurance')
    ])
    payment_status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    ], default='pending')
    
    # Transaction Details
    transaction_id = models.CharField(max_length=200, unique=True, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    
    # Stripe Payment Details
    stripe_payment_intent_id = models.CharField(max_length=200, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=200, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=200, blank=True, null=True)
    
    # Invoice
    invoice_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    invoice_generated = models.BooleanField(default=False)
    
    # Notes
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Payment - {self.patient.name} - ₹{self.amount} - {self.payment_status}"
    
    def save(self, *args, **kwargs):
        # Auto-generate invoice number if not exists
        if not self.invoice_number:
            from datetime import datetime
            self.invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)


# Appointment Feedback
class AppointmentFeedback(models.Model):
    appointment = models.OneToOneField(appointmenthistory, on_delete=models.CASCADE, related_name='feedback')
    patient = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorDetail, on_delete=models.CASCADE)
    
    # Ratings (1-5)
    overall_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    doctor_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    clinic_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    
    # Feedback
    comments = models.TextField(blank=True, null=True)
    would_recommend = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback - {self.patient.name} - Dr. {self.doctor.name}"


# Notification System
class Notification(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    doctor = models.ForeignKey(DoctorDetail, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[
        ('appointment', 'Appointment'),
        ('reminder', 'Reminder'),
        ('payment', 'Payment'),
        ('system', 'System'),
        ('promotion', 'Promotion')
    ])
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        recipient = self.user.name if self.user else self.doctor.name
        return f"Notification - {recipient} - {self.title}"



# ============================================================================
# ADVANCED APPOINTMENT MANAGEMENT
# ============================================================================

# Recurring Appointments
class RecurringAppointment(models.Model):
    FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    ]
    
    patient = models.ForeignKey(UserDetail, on_delete=models.CASCADE, related_name='recurring_appointments')
    doctor = models.ForeignKey(DoctorDetail, on_delete=models.CASCADE, related_name='recurring_appointments')
    
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    time = models.CharField(max_length=20)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient.name} - {self.frequency} with Dr. {self.doctor.name}"


# Appointment Rescheduling History
class AppointmentReschedule(models.Model):
    appointment = models.ForeignKey(bookappointment, on_delete=models.CASCADE, related_name='reschedules')
    old_date = models.CharField(max_length=200)
    old_time = models.CharField(max_length=100)
    new_date = models.CharField(max_length=200)
    new_time = models.CharField(max_length=100)
    reason = models.TextField(blank=True, null=True)
    rescheduled_by = models.CharField(max_length=200)  # patient or doctor
    rescheduled_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Rescheduled: {self.old_date} to {self.new_date}"


# Waitlist Management
class AppointmentWaitlist(models.Model):
    patient = models.ForeignKey(UserDetail, on_delete=models.CASCADE, related_name='waitlist_entries')
    doctor = models.ForeignKey(DoctorDetail, on_delete=models.CASCADE, related_name='waitlist_entries')
    preferred_date = models.DateField()
    preferred_time = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.patient.name} waiting for Dr. {self.doctor.name} on {self.preferred_date}"


# No-show Tracking
class AppointmentNoShow(models.Model):
    appointment = models.OneToOneField(bookappointment, on_delete=models.CASCADE, related_name='no_show')
    patient = models.ForeignKey(UserDetail, on_delete=models.CASCADE, related_name='no_shows')
    doctor = models.ForeignKey(DoctorDetail, on_delete=models.CASCADE, related_name='patient_no_shows')
    
    appointment_date = models.CharField(max_length=200)
    appointment_time = models.CharField(max_length=100)
    marked_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"No-show: {self.patient.name} on {self.appointment_date}"


# Multi-slot Treatment Plans
class TreatmentPlan(models.Model):
    patient = models.ForeignKey(UserDetail, on_delete=models.CASCADE, related_name='treatment_plans')
    doctor = models.ForeignKey(DoctorDetail, on_delete=models.CASCADE, related_name='treatment_plans')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    total_sessions = models.IntegerField()
    completed_sessions = models.IntegerField(default=0)
    
    start_date = models.DateField()
    estimated_end_date = models.DateField()
    
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.patient.name}"


# Treatment Plan Sessions
class TreatmentSession(models.Model):
    treatment_plan = models.ForeignKey(TreatmentPlan, on_delete=models.CASCADE, related_name='sessions')
    session_number = models.IntegerField()
    
    scheduled_date = models.DateField(null=True, blank=True)
    scheduled_time = models.CharField(max_length=100, null=True, blank=True)
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    notes = models.TextField(blank=True, null=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['session_number']
    
    def __str__(self):
        return f"Session {self.session_number} - {self.treatment_plan.title}"



# ============================================================================
# PHASE 4: ENHANCED SECURITY & RBAC
# ============================================================================

# Two-Factor Authentication
class TwoFactorAuth(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE, related_name='two_factor_auth', null=True, blank=True)
    doctor = models.ForeignKey(DoctorDetail, on_delete=models.CASCADE, related_name='two_factor_auth', null=True, blank=True)
    
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        recipient = self.user.email if self.user else self.doctor.email
        return f"2FA - {recipient} - {self.otp_code}"
    
    def is_valid(self):
        """Check if OTP is still valid"""
        from django.utils import timezone
        return not self.is_used and timezone.now() < self.expires_at


# User Roles and Permissions
class UserRole(models.Model):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Administrator'),
        ('staff', 'Staff'),
        ('receptionist', 'Receptionist'),
    ]
    
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE, related_name='roles', null=True, blank=True)
    doctor = models.ForeignKey(DoctorDetail, on_delete=models.CASCADE, related_name='roles', null=True, blank=True)
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        unique_together = ('user', 'doctor', 'role')
    
    def __str__(self):
        recipient = self.user.name if self.user else self.doctor.name
        return f"{recipient} - {self.get_role_display()}"


# Permissions
class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    RESOURCE_CHOICES = [
        ('appointment', 'Appointment'),
        ('medical_record', 'Medical Record'),
        ('payment', 'Payment'),
        ('user', 'User'),
        ('doctor', 'Doctor'),
        ('treatment_plan', 'Treatment Plan'),
        ('system', 'System'),
    ]
    
    resource = models.CharField(max_length=50, choices=RESOURCE_CHOICES)
    
    ACTION_CHOICES = [
        ('view', 'View'),
        ('create', 'Create'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
        ('manage', 'Manage'),
    ]
    
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('resource', 'action')
        ordering = ['resource', 'action']
    
    def __str__(self):
        return f"{self.name} ({self.codename})"


# Role Permissions (Many-to-Many)
class RolePermission(models.Model):
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='roles')
    granted_at = models.DateTimeField(auto_now_add=True)
    granted_by = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        unique_together = ('role', 'permission')
    
    def __str__(self):
        return f"{self.role} - {self.permission.name}"


# Audit Log
class AuditLog(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    doctor = models.ForeignKey(DoctorDetail, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('download', 'Download'),
        ('upload', 'Upload'),
        ('payment', 'Payment'),
        ('failed_login', 'Failed Login'),
        ('password_change', 'Password Change'),
        ('2fa_enable', '2FA Enable'),
        ('2fa_disable', '2FA Disable'),
    ]
    
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    resource_type = models.CharField(max_length=100, blank=True, null=True)  # e.g., 'Appointment', 'MedicalRecord'
    resource_id = models.CharField(max_length=100, blank=True, null=True)
    
    description = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Additional context
    request_method = models.CharField(max_length=10, blank=True, null=True)  # GET, POST, etc.
    request_path = models.CharField(max_length=500, blank=True, null=True)
    status_code = models.IntegerField(blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['action']),
            models.Index(fields=['resource_type']),
        ]
    
    def __str__(self):
        actor = self.user.name if self.user else (self.doctor.name if self.doctor else 'Anonymous')
        return f"{actor} - {self.get_action_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


# API Rate Limiting Tracker
class APIRateLimit(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE, null=True, blank=True, related_name='api_rate_limits')
    doctor = models.ForeignKey(DoctorDetail, on_delete=models.CASCADE, null=True, blank=True, related_name='api_rate_limits')
    ip_address = models.GenericIPAddressField()
    
    endpoint = models.CharField(max_length=200)
    request_count = models.IntegerField(default=0)
    window_start = models.DateTimeField(auto_now_add=True)
    last_request = models.DateTimeField(auto_now=True)
    
    is_blocked = models.BooleanField(default=False)
    blocked_until = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('ip_address', 'endpoint', 'window_start')
        ordering = ['-last_request']
    
    def __str__(self):
        return f"{self.ip_address} - {self.endpoint} - {self.request_count} requests"


# Search History (for advanced search)
class SearchHistory(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE, null=True, blank=True, related_name='search_history')
    doctor = models.ForeignKey(DoctorDetail, on_delete=models.CASCADE, null=True, blank=True, related_name='search_history')
    
    search_query = models.CharField(max_length=500)
    search_type = models.CharField(max_length=50)  # 'doctor', 'appointment', 'medical_record', etc.
    filters = models.JSONField(blank=True, null=True)  # Store filter parameters
    
    results_count = models.IntegerField(default=0)
    searched_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-searched_at']
    
    def __str__(self):
        actor = self.user.name if self.user else (self.doctor.name if self.doctor else 'Anonymous')
        return f"{actor} searched for '{self.search_query}' in {self.search_type}"



# ============================================================================
# PHASE 5: AUTOMATED REPORTS & ANALYTICS
# ============================================================================

# Report Model
class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('daily_appointments', 'Daily Appointments'),
        ('monthly_revenue', 'Monthly Revenue'),
        ('patient_statistics', 'Patient Statistics'),
        ('doctor_performance', 'Doctor Performance'),
        ('appointment_trends', 'Appointment Trends'),
        ('payment_summary', 'Payment Summary'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    generated_by_user = models.ForeignKey(UserDetail, on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_reports')
    generated_by_doctor = models.ForeignKey(DoctorDetail, on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_reports')
    
    file_path = models.CharField(max_length=500, blank=True, null=True)
    file_format = models.CharField(max_length=10, choices=[('pdf', 'PDF'), ('csv', 'CSV'), ('xlsx', 'Excel')], default='pdf')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)
    
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    generated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.get_report_type_display()} - {self.generated_at.strftime('%Y-%m-%d')}"


# Report Schedule
class ReportSchedule(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    report_type = models.CharField(max_length=50, choices=Report.REPORT_TYPE_CHOICES)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    
    recipients = models.TextField(help_text="Comma-separated email addresses")
    
    is_active = models.BooleanField(default=True)
    last_run = models.DateTimeField(blank=True, null=True)
    next_run = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['next_run']
    
    def __str__(self):
        return f"{self.get_report_type_display()} - {self.get_frequency_display()}"


# Analytics Cache (for performance)
class AnalyticsCache(models.Model):
    cache_key = models.CharField(max_length=200, unique=True)
    cache_data = models.JSONField()
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.cache_key} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    def is_valid(self):
        """Check if cache is still valid"""
        from django.utils import timezone
        return timezone.now() < self.expires_at
