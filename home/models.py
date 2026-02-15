
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
