"""
API URL Configuration for Phase 4
REST API endpoints
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from home import api_views

# Create router
router = DefaultRouter()

# Register viewsets
router.register(r'users', api_views.UserViewSet, basename='api-users')
router.register(r'doctors', api_views.DoctorViewSet, basename='api-doctors')
router.register(r'appointments', api_views.AppointmentViewSet, basename='api-appointments')
router.register(r'appointment-history', api_views.AppointmentHistoryViewSet, basename='api-appointment-history')
router.register(r'recurring-appointments', api_views.RecurringAppointmentViewSet, basename='api-recurring-appointments')
router.register(r'waitlist', api_views.WaitlistViewSet, basename='api-waitlist')
router.register(r'medical-records', api_views.MedicalRecordViewSet, basename='api-medical-records')
router.register(r'allergies', api_views.PatientAllergyViewSet, basename='api-allergies')
router.register(r'payments', api_views.PaymentViewSet, basename='api-payments')
router.register(r'ratings', api_views.DoctorRatingViewSet, basename='api-ratings')
router.register(r'notifications', api_views.NotificationViewSet, basename='api-notifications')
router.register(r'treatment-plans', api_views.TreatmentPlanViewSet, basename='api-treatment-plans')
router.register(r'treatment-sessions', api_views.TreatmentSessionViewSet, basename='api-treatment-sessions')

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', api_views.api_register, name='api-register'),
    path('auth/login/', api_views.api_login, name='api-login'),
    path('auth/request-2fa/', api_views.api_request_2fa, name='api-request-2fa'),
    path('auth/verify-2fa/', api_views.api_verify_2fa, name='api-verify-2fa'),
    
    # Search endpoint
    path('search/', api_views.api_search, name='api-search'),
    
    # Statistics endpoint
    path('statistics/', api_views.api_statistics, name='api-statistics'),
    
    # Router URLs
    path('', include(router.urls)),
]
