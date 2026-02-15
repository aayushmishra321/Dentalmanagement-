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



# ============================================================================
# PHASE 3: ADVANCED APPOINTMENT MANAGEMENT ADMIN
# ============================================================================

from home.models import (
    RecurringAppointment, AppointmentReschedule, AppointmentWaitlist,
    AppointmentNoShow, TreatmentPlan, TreatmentSession
)


# Recurring Appointment
@admin.register(RecurringAppointment)
class RecurringAppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'frequency', 'start_date', 'end_date', 'time', 'is_active')
    search_fields = ('patient__name', 'doctor__name')
    list_filter = ('frequency', 'is_active', 'start_date')
    readonly_fields = ('created_at',)


# Appointment Reschedule
@admin.register(AppointmentReschedule)
class AppointmentRescheduleAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'old_date', 'old_time', 'new_date', 'new_time', 'rescheduled_by', 'rescheduled_at')
    search_fields = ('appointment__username', 'appointment__doctorname')
    list_filter = ('rescheduled_by', 'rescheduled_at')
    readonly_fields = ('rescheduled_at',)


# Appointment Waitlist
@admin.register(AppointmentWaitlist)
class AppointmentWaitlistAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'preferred_date', 'preferred_time', 'is_active', 'notified', 'created_at')
    search_fields = ('patient__name', 'doctor__name')
    list_filter = ('is_active', 'notified', 'preferred_date')
    readonly_fields = ('created_at',)


# Appointment No-Show
@admin.register(AppointmentNoShow)
class AppointmentNoShowAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time', 'marked_at')
    search_fields = ('patient__name', 'doctor__name')
    list_filter = ('appointment_date', 'marked_at')
    readonly_fields = ('marked_at',)


# Treatment Plan
@admin.register(TreatmentPlan)
class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'doctor', 'total_sessions', 'completed_sessions', 'total_cost', 'paid_amount', 'is_active')
    search_fields = ('title', 'patient__name', 'doctor__name')
    list_filter = ('is_active', 'start_date', 'created_at')
    readonly_fields = ('created_at',)
    
    def get_progress(self, obj):
        if obj.total_sessions > 0:
            return f"{(obj.completed_sessions / obj.total_sessions * 100):.1f}%"
        return "0%"
    get_progress.short_description = 'Progress'


# Treatment Session
@admin.register(TreatmentSession)
class TreatmentSessionAdmin(admin.ModelAdmin):
    list_display = ('treatment_plan', 'session_number', 'scheduled_date', 'scheduled_time', 'status', 'completed_at')
    search_fields = ('treatment_plan__title', 'treatment_plan__patient__name')
    list_filter = ('status', 'scheduled_date', 'completed_at')
    readonly_fields = ('completed_at',)



# ============================================================================
# PHASE 4: ENHANCED SECURITY & API ADMIN
# ============================================================================

from home.models import (
    TwoFactorAuth, UserRole, Permission, RolePermission,
    AuditLog, APIRateLimit, SearchHistory
)


# Two-Factor Authentication
@admin.register(TwoFactorAuth)
class TwoFactorAuthAdmin(admin.ModelAdmin):
    list_display = ('get_recipient', 'otp_code', 'is_enabled', 'is_used', 'created_at', 'expires_at')
    search_fields = ('user__email', 'doctor__email', 'otp_code')
    list_filter = ('is_enabled', 'is_used', 'created_at')
    readonly_fields = ('created_at', 'expires_at')
    
    def get_recipient(self, obj):
        if obj.user:
            return f"Patient: {obj.user.email}"
        elif obj.doctor:
            return f"Doctor: {obj.doctor.email}"
        return "N/A"
    get_recipient.short_description = 'Recipient'


# User Roles
@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'role', 'is_active', 'assigned_at', 'assigned_by')
    search_fields = ('user__name', 'doctor__name', 'role')
    list_filter = ('role', 'is_active', 'assigned_at')
    readonly_fields = ('assigned_at',)
    
    def get_user(self, obj):
        if obj.user:
            return f"{obj.user.name} (Patient)"
        elif obj.doctor:
            return f"{obj.doctor.name} (Doctor)"
        return "N/A"
    get_user.short_description = 'User'


# Permissions
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename', 'resource', 'action', 'created_at')
    search_fields = ('name', 'codename', 'description')
    list_filter = ('resource', 'action', 'created_at')
    readonly_fields = ('created_at',)


# Role Permissions
@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission', 'granted_at', 'granted_by')
    search_fields = ('role__role', 'permission__name')
    list_filter = ('granted_at',)
    readonly_fields = ('granted_at',)


# Audit Log
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('get_actor', 'action', 'resource_type', 'ip_address', 'timestamp', 'status_code')
    search_fields = ('user__name', 'doctor__name', 'action', 'resource_type', 'ip_address')
    list_filter = ('action', 'resource_type', 'timestamp', 'status_code')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    
    def get_actor(self, obj):
        if obj.user:
            return f"Patient: {obj.user.name}"
        elif obj.doctor:
            return f"Doctor: {obj.doctor.name}"
        return "Anonymous"
    get_actor.short_description = 'Actor'
    
    def has_add_permission(self, request):
        return False  # Audit logs should not be manually created
    
    def has_change_permission(self, request, obj=None):
        return False  # Audit logs should not be modified


# API Rate Limit
@admin.register(APIRateLimit)
class APIRateLimitAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'endpoint', 'request_count', 'is_blocked', 'last_request')
    search_fields = ('ip_address', 'endpoint')
    list_filter = ('is_blocked', 'last_request')
    readonly_fields = ('window_start', 'last_request')


# Search History
@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'search_query', 'search_type', 'results_count', 'searched_at')
    search_fields = ('user__name', 'doctor__name', 'search_query', 'search_type')
    list_filter = ('search_type', 'searched_at')
    readonly_fields = ('searched_at',)
    date_hierarchy = 'searched_at'
    
    def get_user(self, obj):
        if obj.user:
            return f"{obj.user.name} (Patient)"
        elif obj.doctor:
            return f"{obj.doctor.name} (Doctor)"
        return "Anonymous"
    get_user.short_description = 'User'



# ============================================================================
# PHASE 5: REPORTS & ANALYTICS ADMIN
# ============================================================================

from home.models import Report, ReportSchedule, AnalyticsCache


# Report
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'file_format', 'status', 'title', 'generated_at')
    search_fields = ('report_type', 'title')
    list_filter = ('report_type', 'file_format', 'status', 'generated_at')
    readonly_fields = ('generated_at',)
    date_hierarchy = 'generated_at'


# Report Schedule
@admin.register(ReportSchedule)
class ReportScheduleAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'frequency', 'is_active', 'last_run', 'next_run')
    search_fields = ('report_type', 'recipients')
    list_filter = ('frequency', 'is_active', 'last_run')
    readonly_fields = ('last_run', 'created_at')


# Analytics Cache
@admin.register(AnalyticsCache)
class AnalyticsCacheAdmin(admin.ModelAdmin):
    list_display = ('cache_key', 'created_at', 'expires_at')
    search_fields = ('cache_key',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    
    def has_add_permission(self, request):
        return False  # Cache entries should be auto-generated
