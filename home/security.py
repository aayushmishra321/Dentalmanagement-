"""
Security utilities for Phase 4: Enhanced Security
Includes 2FA, audit logging, permissions, and rate limiting
"""

import random
import string
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from home.models import TwoFactorAuth, AuditLog, UserRole, Permission, RolePermission
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# TWO-FACTOR AUTHENTICATION (2FA)
# ============================================================================

def generate_otp(length=6):
    """Generate a random OTP code"""
    return ''.join(random.choices(string.digits, k=length))


def create_2fa_otp(user=None, doctor=None):
    """Create and send 2FA OTP"""
    if not user and not doctor:
        raise ValueError("Either user or doctor must be provided")
    
    # Generate OTP
    otp_code = generate_otp(settings.TWO_FACTOR_OTP_LENGTH)
    
    # Calculate expiry
    expires_at = timezone.now() + timedelta(seconds=settings.TWO_FACTOR_OTP_EXPIRY)
    
    # Create 2FA record
    two_factor = TwoFactorAuth.objects.create(
        user=user,
        doctor=doctor,
        otp_code=otp_code,
        expires_at=expires_at,
        is_used=False
    )
    
    # Send OTP via email
    recipient_email = user.email if user else doctor.email
    recipient_name = user.name if user else doctor.name
    
    try:
        send_mail(
            'Your Login OTP',
            f'Hi {recipient_name},\n\nYour OTP for login is: {otp_code}\n\nThis OTP will expire in {settings.TWO_FACTOR_OTP_EXPIRY // 60} minutes.\n\nIf you did not request this, please ignore this email.\n\nThank you,\nDental Management System',
            settings.EMAIL_HOST_USER,
            [recipient_email],
            fail_silently=False,
        )
        logger.info(f"2FA OTP sent to {recipient_email}")
        return two_factor
    except Exception as e:
        logger.error(f"Failed to send 2FA OTP: {str(e)}")
        two_factor.delete()
        raise


def verify_2fa_otp(otp_code, user=None, doctor=None):
    """Verify 2FA OTP"""
    try:
        # Find the OTP
        query = TwoFactorAuth.objects.filter(
            otp_code=otp_code,
            is_used=False
        )
        
        if user:
            query = query.filter(user=user)
        elif doctor:
            query = query.filter(doctor=doctor)
        else:
            return False
        
        two_factor = query.first()
        
        if not two_factor:
            return False
        
        # Check if OTP is valid
        if not two_factor.is_valid():
            return False
        
        # Mark as used
        two_factor.is_used = True
        two_factor.save()
        
        return True
        
    except Exception as e:
        logger.error(f"Error verifying 2FA OTP: {str(e)}")
        return False


def enable_2fa(user=None, doctor=None):
    """Enable 2FA for user or doctor"""
    if user:
        TwoFactorAuth.objects.filter(user=user).update(is_enabled=True)
    elif doctor:
        TwoFactorAuth.objects.filter(doctor=doctor).update(is_enabled=True)


def disable_2fa(user=None, doctor=None):
    """Disable 2FA for user or doctor"""
    if user:
        TwoFactorAuth.objects.filter(user=user).update(is_enabled=False)
    elif doctor:
        TwoFactorAuth.objects.filter(doctor=doctor).update(is_enabled=False)


def is_2fa_enabled(user=None, doctor=None):
    """Check if 2FA is enabled"""
    try:
        if user:
            two_factor = TwoFactorAuth.objects.filter(user=user, is_enabled=True).first()
        elif doctor:
            two_factor = TwoFactorAuth.objects.filter(doctor=doctor, is_enabled=True).first()
        else:
            return False
        
        return two_factor is not None
    except:
        return False


# ============================================================================
# AUDIT LOGGING
# ============================================================================

def log_audit(request, action, resource_type=None, resource_id=None, description=None, status_code=200):
    """Create audit log entry"""
    if not settings.AUDIT_LOG_ENABLED:
        return
    
    # Get user/doctor from session
    user = None
    doctor = None
    
    if request.session.get('user_logged_in'):
        from home.models import UserDetail
        try:
            user = UserDetail.objects.get(email=request.session.get('user_email'))
        except:
            pass
    elif request.session.get('doctor_logged_in'):
        from home.models import DoctorDetail
        try:
            doctor = DoctorDetail.objects.get(email=request.session.get('doctor_email'))
        except:
            pass
    
    # Skip if anonymous and not logging anonymous
    if not user and not doctor and not settings.AUDIT_LOG_ANONYMOUS:
        return
    
    # Skip excluded paths
    for excluded_path in settings.AUDIT_LOG_EXCLUDE_PATHS:
        if request.path.startswith(excluded_path):
            return
    
    # Get IP address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    
    # Create audit log
    try:
        AuditLog.objects.create(
            user=user,
            doctor=doctor,
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id) if resource_id else None,
            description=description,
            ip_address=ip_address,
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            request_method=request.method,
            request_path=request.path,
            status_code=status_code
        )
        logger.debug(f"Audit log created: {action} by {user or doctor or 'Anonymous'}")
    except Exception as e:
        logger.error(f"Failed to create audit log: {str(e)}")


# ============================================================================
# ROLE-BASED ACCESS CONTROL (RBAC)
# ============================================================================

def assign_role(user=None, doctor=None, role='patient', assigned_by=None):
    """Assign role to user or doctor"""
    try:
        user_role, created = UserRole.objects.get_or_create(
            user=user,
            doctor=doctor,
            role=role,
            defaults={'assigned_by': assigned_by, 'is_active': True}
        )
        
        if not created:
            user_role.is_active = True
            user_role.save()
        
        return user_role
    except Exception as e:
        logger.error(f"Failed to assign role: {str(e)}")
        return None


def remove_role(user=None, doctor=None, role=None):
    """Remove role from user or doctor"""
    try:
        query = UserRole.objects.filter(is_active=True)
        
        if user:
            query = query.filter(user=user)
        elif doctor:
            query = query.filter(doctor=doctor)
        
        if role:
            query = query.filter(role=role)
        
        query.update(is_active=False)
        return True
    except Exception as e:
        logger.error(f"Failed to remove role: {str(e)}")
        return False


def has_role(user=None, doctor=None, role=None):
    """Check if user/doctor has specific role"""
    try:
        query = UserRole.objects.filter(is_active=True)
        
        if user:
            query = query.filter(user=user)
        elif doctor:
            query = query.filter(doctor=doctor)
        else:
            return False
        
        if role:
            query = query.filter(role=role)
        
        return query.exists()
    except:
        return False


def get_user_roles(user=None, doctor=None):
    """Get all roles for user or doctor"""
    try:
        query = UserRole.objects.filter(is_active=True)
        
        if user:
            query = query.filter(user=user)
        elif doctor:
            query = query.filter(doctor=doctor)
        else:
            return []
        
        return list(query.values_list('role', flat=True))
    except:
        return []


def has_permission(user=None, doctor=None, permission_codename=None):
    """Check if user/doctor has specific permission"""
    try:
        # Get user roles
        roles = UserRole.objects.filter(is_active=True)
        
        if user:
            roles = roles.filter(user=user)
        elif doctor:
            roles = roles.filter(doctor=doctor)
        else:
            return False
        
        # Check if any role has the permission
        for role in roles:
            if RolePermission.objects.filter(
                role=role,
                permission__codename=permission_codename
            ).exists():
                return True
        
        return False
    except:
        return False


# ============================================================================
# DECORATORS
# ============================================================================

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def require_role(role):
    """Decorator to require specific role"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = None
            doctor = None
            
            if request.session.get('user_logged_in'):
                from home.models import UserDetail
                try:
                    user = UserDetail.objects.get(email=request.session.get('user_email'))
                except:
                    pass
            elif request.session.get('doctor_logged_in'):
                from home.models import DoctorDetail
                try:
                    doctor = DoctorDetail.objects.get(email=request.session.get('doctor_email'))
                except:
                    pass
            
            if not has_role(user=user, doctor=doctor, role=role):
                messages.error(request, f"You need {role} role to access this page")
                return redirect('home')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_permission(permission_codename):
    """Decorator to require specific permission"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = None
            doctor = None
            
            if request.session.get('user_logged_in'):
                from home.models import UserDetail
                try:
                    user = UserDetail.objects.get(email=request.session.get('user_email'))
                except:
                    pass
            elif request.session.get('doctor_logged_in'):
                from home.models import DoctorDetail
                try:
                    doctor = DoctorDetail.objects.get(email=request.session.get('doctor_email'))
                except:
                    pass
            
            if not has_permission(user=user, doctor=doctor, permission_codename=permission_codename):
                messages.error(request, "You don't have permission to access this page")
                return redirect('home')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_2fa(view_func):
    """Decorator to require 2FA verification"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if 2FA is verified in session
        if not request.session.get('2fa_verified', False):
            messages.warning(request, "Please verify your identity with 2FA")
            return redirect('verify_2fa')
        
        return view_func(request, *args, **kwargs)
    return wrapper
