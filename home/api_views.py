"""
REST API Views for Phase 4
Complete API endpoints for all features
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from home.models import (
    UserDetail, DoctorDetail, bookappointment, appointmenthistory,
    DoctorRating, MedicalRecord, PatientAllergy, Payment,
    Notification, RecurringAppointment, AppointmentWaitlist,
    TreatmentPlan, TreatmentSession
)
from home.serializers import *
from home.security import create_2fa_otp, verify_2fa_otp, log_audit


# ============================================================================
# AUTHENTICATION API
# ============================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    """Register new user"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        try:
            # Create user
            user = UserDetail.objects.create(
                name=serializer.validated_data['name'],
                email=serializer.validated_data['email'],
                contact=serializer.validated_data['contact'],
                dateofbirth=serializer.validated_data['dateofbirth'],
                gender=serializer.validated_data['gender'],
                address=serializer.validated_data['address'],
                pincode=serializer.validated_data['pincode'],
                password=serializer.validated_data['password']
            )
            
            return Response({
                'message': 'Registration successful',
                'user': UserDetailSerializer(user).data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """Login and get JWT tokens"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user_type = serializer.validated_data['user_type']
        
        try:
            if user_type == 'patient':
                user = UserDetail.objects.get(email=email)
                if user.password == password:
                    # Generate tokens (simplified - in production use proper JWT)
                    return Response({
                        'message': 'Login successful',
                        'user_type': 'patient',
                        'user': UserDetailSerializer(user).data,
                        'email': email
                    })
            else:
                doctor = DoctorDetail.objects.get(email=email)
                if doctor.password == password:
                    return Response({
                        'message': 'Login successful',
                        'user_type': 'doctor',
                        'user': DoctorDetailSerializer(doctor).data,
                        'email': email
                    })
            
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        except (UserDetail.DoesNotExist, DoctorDetail.DoesNotExist):
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_request_2fa(request):
    """Request 2FA OTP"""
    email = request.data.get('email')
    user_type = request.data.get('user_type', 'patient')
    
    try:
        if user_type == 'patient':
            user = UserDetail.objects.get(email=email)
            create_2fa_otp(user=user)
        else:
            doctor = DoctorDetail.objects.get(email=email)
            create_2fa_otp(doctor=doctor)
        
        return Response({
            'message': 'OTP sent to your email'
        })
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_verify_2fa(request):
    """Verify 2FA OTP"""
    serializer = TwoFactorVerifySerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        user_type = serializer.validated_data['user_type']
        
        try:
            if user_type == 'patient':
                user = UserDetail.objects.get(email=email)
                if verify_2fa_otp(otp_code, user=user):
                    return Response({'message': '2FA verified successfully'})
            else:
                doctor = DoctorDetail.objects.get(email=email)
                if verify_2fa_otp(otp_code, doctor=doctor):
                    return Response({'message': '2FA verified successfully'})
            
            return Response({
                'error': 'Invalid or expired OTP'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================================================
# USER & DOCTOR VIEWSETS
# ============================================================================

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for users"""
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'email', 'contact']
    lookup_field = 'email'


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for doctors"""
    queryset = DoctorDetail.objects.all()
    serializer_class = DoctorDetailSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city', 'clinicname']
    filterset_fields = ['city', 'experience']
    ordering_fields = ['consultationfee', 'name']
    lookup_field = 'email'


# ============================================================================
# APPOINTMENT VIEWSETS
# ============================================================================

class AppointmentViewSet(viewsets.ModelViewSet):
    """API endpoint for appointments"""
    queryset = bookappointment.objects.all()
    serializer_class = BookAppointmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['useremail', 'doctoremail', 'appdate', 'payment']
    search_fields = ['username', 'doctorname']


class AppointmentHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for appointment history"""
    queryset = appointmenthistory.objects.all()
    serializer_class = AppointmentHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['useremail', 'doctoremail', 'appdate']


class RecurringAppointmentViewSet(viewsets.ModelViewSet):
    """API endpoint for recurring appointments"""
    queryset = RecurringAppointment.objects.all()
    serializer_class = RecurringAppointmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient__email', 'doctor__email', 'frequency', 'is_active']


class WaitlistViewSet(viewsets.ModelViewSet):
    """API endpoint for waitlist"""
    queryset = AppointmentWaitlist.objects.all()
    serializer_class = AppointmentWaitlistSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient__email', 'doctor__email', 'is_active']


# ============================================================================
# MEDICAL RECORDS VIEWSETS
# ============================================================================

class MedicalRecordViewSet(viewsets.ModelViewSet):
    """API endpoint for medical records"""
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient__email', 'doctor__email', 'follow_up_required']


class PatientAllergyViewSet(viewsets.ModelViewSet):
    """API endpoint for patient allergies"""
    queryset = PatientAllergy.objects.all()
    serializer_class = PatientAllergySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient__email', 'severity']


# ============================================================================
# PAYMENT VIEWSETS
# ============================================================================

class PaymentViewSet(viewsets.ModelViewSet):
    """API endpoint for payments"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient__email', 'doctor__email', 'payment_status', 'payment_method']


# ============================================================================
# RATING VIEWSETS
# ============================================================================

class DoctorRatingViewSet(viewsets.ModelViewSet):
    """API endpoint for doctor ratings"""
    queryset = DoctorRating.objects.all()
    serializer_class = DoctorRatingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor__email', 'patient__email', 'rating', 'is_verified']


# ============================================================================
# NOTIFICATION VIEWSETS
# ============================================================================

class NotificationViewSet(viewsets.ModelViewSet):
    """API endpoint for notifications"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__email', 'doctor__email', 'is_read', 'notification_type']


# ============================================================================
# TREATMENT PLAN VIEWSETS
# ============================================================================

class TreatmentPlanViewSet(viewsets.ModelViewSet):
    """API endpoint for treatment plans"""
    queryset = TreatmentPlan.objects.all()
    serializer_class = TreatmentPlanSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient__email', 'doctor__email', 'is_active']


class TreatmentSessionViewSet(viewsets.ModelViewSet):
    """API endpoint for treatment sessions"""
    queryset = TreatmentSession.objects.all()
    serializer_class = TreatmentSessionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['treatment_plan__id', 'status']


# ============================================================================
# SEARCH API
# ============================================================================

@api_view(['GET'])
def api_search(request):
    """Advanced search across all resources"""
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')
    
    results = {}
    
    if search_type in ['all', 'doctors']:
        doctors = DoctorDetail.objects.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query) |
            Q(clinicname__icontains=query)
        )[:10]
        results['doctors'] = DoctorDetailSerializer(doctors, many=True).data
    
    if search_type in ['all', 'appointments']:
        appointments = bookappointment.objects.filter(
            Q(username__icontains=query) |
            Q(doctorname__icontains=query)
        )[:10]
        results['appointments'] = BookAppointmentSerializer(appointments, many=True).data
    
    return Response(results)


# ============================================================================
# STATISTICS API
# ============================================================================

@api_view(['GET'])
def api_statistics(request):
    """Get system statistics"""
    stats = {
        'total_users': UserDetail.objects.count(),
        'total_doctors': DoctorDetail.objects.count(),
        'total_appointments': bookappointment.objects.count(),
        'total_payments': Payment.objects.filter(payment_status='completed').count(),
        'total_medical_records': MedicalRecord.objects.count(),
        'total_treatment_plans': TreatmentPlan.objects.filter(is_active=True).count(),
    }
    
    return Response(stats)
