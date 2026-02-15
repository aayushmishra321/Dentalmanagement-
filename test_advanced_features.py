"""
Test Script for Advanced Features
Tests all newly implemented features
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dentalmanagement.settings')
django.setup()

from home.models import (
    UserDetail, DoctorDetail, bookappointment, appointmenthistory,
    DoctorRating, MedicalRecord, MedicalImage, PatientAllergy,
    Payment, AppointmentFeedback, Notification
)
from django.test import Client

class AdvancedFeaturesTest:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        
    def log(self, message, status="INFO"):
        symbols = {"PASS": "✓", "FAIL": "✗", "INFO": "ℹ"}
        print(f"{symbols.get(status, '•')} {message}")
    
    def test_new_models(self):
        """Test all new models are created"""
        self.log("\n=== Testing New Models ===", "INFO")
        
        models_to_test = [
            ('DoctorRating', DoctorRating),
            ('MedicalRecord', MedicalRecord),
            ('MedicalImage', MedicalImage),
            ('PatientAllergy', PatientAllergy),
            ('Payment', Payment),
            ('AppointmentFeedback', AppointmentFeedback),
            ('Notification', Notification),
        ]
        
        for model_name, model_class in models_to_test:
            try:
                count = model_class.objects.count()
                self.log(f"Model {model_name}: Accessible ({count} records)", "PASS")
                self.passed += 1
            except Exception as e:
                self.log(f"Model {model_name}: Error - {str(e)}", "FAIL")
                self.failed += 1
                self.errors.append(f"Model {model_name}: {str(e)}")
    
    def test_celery_configuration(self):
        """Test Celery is configured"""
        self.log("\n=== Testing Celery Configuration ===", "INFO")
        
        try:
            from dentalmanagement.celery import app
            self.log("Celery app: Configured", "PASS")
            self.passed += 1
        except Exception as e:
            self.log(f"Celery app: Error - {str(e)}", "FAIL")
            self.failed += 1
            self.errors.append(f"Celery: {str(e)}")
        
        try:
            from home import tasks
            self.log("Celery tasks: Imported successfully", "PASS")
            self.passed += 1
        except Exception as e:
            self.log(f"Celery tasks: Error - {str(e)}", "FAIL")
            self.failed += 1
            self.errors.append(f"Tasks: {str(e)}")
    
    def test_rest_framework(self):
        """Test Django REST Framework is configured"""
        self.log("\n=== Testing REST Framework ===", "INFO")
        
        try:
            from rest_framework import status
            self.log("REST Framework: Installed", "PASS")
            self.passed += 1
        except Exception as e:
            self.log(f"REST Framework: Error - {str(e)}", "FAIL")
            self.failed += 1
            self.errors.append(f"REST Framework: {str(e)}")
    
    def test_admin_registrations(self):
        """Test all models are registered in admin"""
        self.log("\n=== Testing Admin Registrations ===", "INFO")
        
        try:
            from django.contrib import admin
            from home.admin import (
                DoctorRatingAdmin, MedicalRecordAdmin, PaymentAdmin,
                NotificationAdmin, AppointmentFeedbackAdmin
            )
            self.log("Admin classes: All imported successfully", "PASS")
            self.passed += 1
        except Exception as e:
            self.log(f"Admin classes: Error - {str(e)}", "FAIL")
            self.failed += 1
            self.errors.append(f"Admin: {str(e)}")
    
    def test_settings_configuration(self):
        """Test settings are properly configured"""
        self.log("\n=== Testing Settings Configuration ===", "INFO")
        
        from django.conf import settings
        
        # Test Celery settings
        if hasattr(settings, 'CELERY_BROKER_URL'):
            self.log("Celery broker URL: Configured", "PASS")
            self.passed += 1
        else:
            self.log("Celery broker URL: Not configured", "FAIL")
            self.failed += 1
        
        # Test REST Framework settings
        if hasattr(settings, 'REST_FRAMEWORK'):
            self.log("REST Framework settings: Configured", "PASS")
            self.passed += 1
        else:
            self.log("REST Framework settings: Not configured", "FAIL")
            self.failed += 1
        
        # Test Media settings
        if hasattr(settings, 'MEDIA_URL') and hasattr(settings, 'MEDIA_ROOT'):
            self.log("Media settings: Configured", "PASS")
            self.passed += 1
        else:
            self.log("Media settings: Not configured", "FAIL")
            self.failed += 1
    
    def test_installed_apps(self):
        """Test all new apps are installed"""
        self.log("\n=== Testing Installed Apps ===", "INFO")
        
        from django.conf import settings
        
        required_apps = [
            'rest_framework',
            'django_filters',
            'corsheaders',
            'django_celery_beat',
            'django_celery_results',
            'django_cleanup.apps.CleanupConfig',
            'star_ratings',
            'import_export',
        ]
        
        for app in required_apps:
            if app in settings.INSTALLED_APPS:
                self.log(f"App '{app}': Installed", "PASS")
                self.passed += 1
            else:
                self.log(f"App '{app}': Not installed", "FAIL")
                self.failed += 1
                self.errors.append(f"App {app} not in INSTALLED_APPS")
    
    def test_database_tables(self):
        """Test new database tables exist"""
        self.log("\n=== Testing Database Tables ===", "INFO")
        
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = [
            'home_doctorrating',
            'home_medicalrecord',
            'home_medicalimage',
            'home_patientallergy',
            'home_payment',
            'home_appointmentfeedback',
            'home_notification',
        ]
        
        for table in required_tables:
            if table in tables:
                self.log(f"Table '{table}': Exists", "PASS")
                self.passed += 1
            else:
                self.log(f"Table '{table}': Missing", "FAIL")
                self.failed += 1
                self.errors.append(f"Table {table} not found")
    
    def test_model_relationships(self):
        """Test model relationships work"""
        self.log("\n=== Testing Model Relationships ===", "INFO")
        
        try:
            # Test if we can access related fields
            users = UserDetail.objects.all()
            if users.exists():
                user = users.first()
                # Test relationships
                _ = user.medical_records.all()
                _ = user.allergies.all()
                _ = user.payments.all()
                _ = user.notifications.all()
                self.log("User model relationships: Working", "PASS")
                self.passed += 1
            else:
                self.log("User model relationships: No users to test", "INFO")
                self.passed += 1
        except Exception as e:
            self.log(f"User model relationships: Error - {str(e)}", "FAIL")
            self.failed += 1
            self.errors.append(f"Relationships: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests"""
        self.log("\n" + "="*60, "INFO")
        self.log("ADVANCED FEATURES TESTING", "INFO")
        self.log("="*60, "INFO")
        
        self.test_new_models()
        self.test_celery_configuration()
        self.test_rest_framework()
        self.test_admin_registrations()
        self.test_settings_configuration()
        self.test_installed_apps()
        self.test_database_tables()
        self.test_model_relationships()
        
        # Print summary
        self.log("\n" + "="*60, "INFO")
        self.log("TEST SUMMARY", "INFO")
        self.log("="*60, "INFO")
        self.log(f"Total Tests Passed: {self.passed}", "PASS")
        if self.failed > 0:
            self.log(f"Total Tests Failed: {self.failed}", "FAIL")
        else:
            self.log(f"Total Tests Failed: {self.failed}", "INFO")
        
        if self.passed + self.failed > 0:
            success_rate = (self.passed/(self.passed+self.failed)*100)
            self.log(f"Success Rate: {success_rate:.1f}%", "INFO")
        
        if self.errors:
            self.log("\n=== ERRORS ENCOUNTERED ===", "INFO")
            for error in self.errors:
                self.log(error, "FAIL")
        
        self.log("\n" + "="*60, "INFO")
        if self.failed == 0:
            self.log("ALL ADVANCED FEATURES TESTS PASSED! ✓", "PASS")
        else:
            self.log(f"TESTING COMPLETE WITH {self.failed} FAILURES", "INFO")
        self.log("="*60, "INFO")

if __name__ == '__main__':
    tester = AdvancedFeaturesTest()
    tester.run_all_tests()
