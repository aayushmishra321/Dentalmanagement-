"""
REST API Serializers for Phase 4
Complete API serializers for all models
"""

from rest_framework import serializers
from home.models import (
    UserDetail, DoctorDetail, bookappointment, appointmenthistory,
    DoctorRating, MedicalRecord, MedicalImage, PatientAllergy,
    Payment, AppointmentFeedback, Notification,
    RecurringAppointment, AppointmentReschedule, AppointmentWaitlist,
    AppointmentNoShow, TreatmentPlan, TreatmentSession,
    TwoFactorAuth, UserRole, AuditLog
)


# ============================================================================
# USER & DOCTOR SERIALIZERS
# ============================================================================

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ['name', 'email', 'contact', 'dateofbirth', 'gender', 'address', 'pincode']
        extra_kwargs = {'password': {'write_only': True}}


class DoctorDetailSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    total_ratings = serializers.SerializerMethodField()
    
    class Meta:
        model = DoctorDetail
        fields = ['name', 'email', 'contact', 'experience', 'clinicname', 'city', 
                  'consultationfee', 'average_rating', 'total_ratings']
        extra_kwargs = {'password': {'write_only': True}}
    
    def get_average_rating(self, obj):
        from home.utils import calculate_doctor_average_rating
        return calculate_doctor_average_rating(obj)
    
    def get_total_ratings(self, obj):
        return DoctorRating.objects.filter(doctor=obj, is_verified=True).count()


# ============================================================================
# APPOINTMENT SERIALIZERS
# ============================================================================

class BookAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = bookappointment
        fields = '__all__'


class AppointmentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = appointmenthistory
        fields = '__all__'


class RecurringAppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    
    class Meta:
        model = RecurringAppointment
        fields = '__all__'


class AppointmentRescheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentReschedule
        fields = '__all__'


class AppointmentWaitlistSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    
    class Meta:
        model = AppointmentWaitlist
        fields = '__all__'


class AppointmentNoShowSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    
    class Meta:
        model = AppointmentNoShow
        fields = '__all__'


# ============================================================================
# MEDICAL RECORDS SERIALIZERS
# ============================================================================

class MedicalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalImage
        fields = '__all__'


class MedicalRecordSerializer(serializers.ModelSerializer):
    images = MedicalImageSerializer(many=True, read_only=True)
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = '__all__'


class PatientAllergySerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    
    class Meta:
        model = PatientAllergy
        fields = '__all__'


# ============================================================================
# PAYMENT SERIALIZERS
# ============================================================================

class PaymentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'


# ============================================================================
# RATING & FEEDBACK SERIALIZERS
# ============================================================================

class DoctorRatingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    
    class Meta:
        model = DoctorRating
        fields = '__all__'


class AppointmentFeedbackSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    
    class Meta:
        model = AppointmentFeedback
        fields = '__all__'


# ============================================================================
# NOTIFICATION SERIALIZERS
# ============================================================================

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


# ============================================================================
# TREATMENT PLAN SERIALIZERS
# ============================================================================

class TreatmentSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentSession
        fields = '__all__'


class TreatmentPlanSerializer(serializers.ModelSerializer):
    sessions = TreatmentSessionSerializer(many=True, read_only=True)
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = TreatmentPlan
        fields = '__all__'
    
    def get_progress_percentage(self, obj):
        if obj.total_sessions > 0:
            return (obj.completed_sessions / obj.total_sessions * 100)
        return 0


# ============================================================================
# SECURITY SERIALIZERS
# ============================================================================

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class AuditLogSerializer(serializers.ModelSerializer):
    actor = serializers.SerializerMethodField()
    
    class Meta:
        model = AuditLog
        fields = '__all__'
    
    def get_actor(self, obj):
        if obj.user:
            return f"Patient: {obj.user.name}"
        elif obj.doctor:
            return f"Doctor: {obj.doctor.name}"
        return "Anonymous"


# ============================================================================
# AUTHENTICATION SERIALIZERS
# ============================================================================

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=['patient', 'doctor'])


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    contact = serializers.CharField(max_length=12)
    dateofbirth = serializers.CharField(max_length=200)
    gender = serializers.CharField(max_length=50)
    address = serializers.CharField()
    pincode = serializers.CharField(max_length=10)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data


class TwoFactorVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)
    user_type = serializers.ChoiceField(choices=['patient', 'doctor'])
