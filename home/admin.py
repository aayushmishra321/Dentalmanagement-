from django.contrib import admin
from home.models import (
    UserDetail, UserContacts, appointmenthistory, DoctorsMessage, 
    DoctorDetail, bookappointment, DoctorRating, MedicalRecord, 
    MedicalImage, PatientAllergy, Payment, AppointmentFeedback, Notification
)
from import_export.admin import ImportExportModelAdmin

# Register your models here.

# User detail with import/export
@admin.register(UserDetail)
class UserDetailAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'contact', 'gender', 'dateofbirth')
    search_fields = ('name', 'email', 'contact')
    list_filter = ('gender',)


# User contact
@admin.register(UserContacts)
class UserContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact', 'message', 'date')
    search_fields = ('name', 'email')
    list_filter = ('date',)


# Doctor contact
@admin.register(DoctorsMessage)
class DoctorsContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact', 'message', 'date')
    search_fields = ('name', 'email')
    list_filter = ('date',)


# Doctor detail with import/export
@admin.register(DoctorDetail)
class DoctorDetailAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'contact', 'experience', 'clinicname', 'city', 'consultationfee')
    search_fields = ('name', 'email', 'city', 'clinicname')
    list_filter = ('city', 'experience')


# Appointment
@admin.register(bookappointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('username', 'useremail', 'doctorname', 'doctoremail', 'appdate', 'apptime', 'consultationfee', 'payment')
    search_fields = ('username', 'useremail', 'doctorname', 'doctoremail')
    list_filter = ('appdate', 'payment')


# Appointment history
@admin.register(appointmenthistory)
class AppointmentHistoryAdmin(ImportExportModelAdmin):
    list_display = ('username', 'useremail', 'doctorname', 'doctoremail', 'appdate', 'apptime', 'consultationfee', 'payment')
    search_fields = ('username', 'useremail', 'doctorname', 'doctoremail')
    list_filter = ('appdate', 'payment')


# ============================================================================
# ADVANCED FEATURES ADMIN
# ============================================================================

# Doctor Rating
@admin.register(DoctorRating)
class DoctorRatingAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'rating', 'is_verified', 'created_at')
    search_fields = ('doctor__name', 'patient__name')
    list_filter = ('rating', 'is_verified', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


# Medical Record
@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'diagnosis', 'procedure_type', 'follow_up_required', 'created_at')
    search_fields = ('patient__name', 'doctor__name', 'diagnosis')
    list_filter = ('follow_up_required', 'procedure_type', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


# Medical Image
@admin.register(MedicalImage)
class MedicalImageAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'image_type', 'uploaded_at')
    search_fields = ('medical_record__patient__name',)
    list_filter = ('image_type', 'uploaded_at')
    readonly_fields = ('uploaded_at',)


# Patient Allergy
@admin.register(PatientAllergy)
class PatientAllergyAdmin(admin.ModelAdmin):
    list_display = ('patient', 'allergy_name', 'severity', 'added_date')
    search_fields = ('patient__name', 'allergy_name')
    list_filter = ('severity', 'added_date')
    readonly_fields = ('added_date',)


# Payment
@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin):
    list_display = ('patient', 'doctor', 'amount', 'payment_method', 'payment_status', 'invoice_number', 'payment_date')
    search_fields = ('patient__name', 'doctor__name', 'invoice_number', 'transaction_id')
    list_filter = ('payment_status', 'payment_method', 'payment_date')
    readonly_fields = ('payment_date', 'invoice_number')
    date_hierarchy = 'payment_date'


# Appointment Feedback
@admin.register(AppointmentFeedback)
class AppointmentFeedbackAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'overall_rating', 'would_recommend', 'created_at')
    search_fields = ('patient__name', 'doctor__name')
    list_filter = ('overall_rating', 'would_recommend', 'created_at')
    readonly_fields = ('created_at',)


# Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('get_recipient', 'title', 'notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message')
    list_filter = ('notification_type', 'is_read', 'created_at')
    readonly_fields = ('created_at',)
    
    def get_recipient(self, obj):
        if obj.user:
            return f"Patient: {obj.user.name}"
        elif obj.doctor:
            return f"Doctor: {obj.doctor.name}"
        return "N/A"
    get_recipient.short_description = 'Recipient'