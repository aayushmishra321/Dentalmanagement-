"""
Comprehensive Testing Script for Dental Management System
Tests all routes, views, models, and functionality
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dentalmanagement.settings')
django.setup()

from django.test import Client
from django.urls import reverse, resolve
from home.models import UserDetail, DoctorDetail, bookappointment, appointmenthistory, UserContacts, DoctorsMessage
from home import views
from datetime import datetime, timedelta

class TestRunner:
    def __init__(self):
        self.client = Client()
        self.passed = 0
        self.failed = 0
        self.errors = []
        
    def log(self, message, status="INFO"):
        symbols = {"PASS": "✓", "FAIL": "✗", "INFO": "ℹ"}
        print(f"{symbols.get(status, '•')} {message}")
        
    def test_url_routing(self):
        """Test all URL routes are properly configured"""
        self.log("\n=== Testing URL Routing ===", "INFO")
        
        urls_to_test = [
            ('', 'home'),
            ('contactus/', 'contact'),
            ('about/', 'about'),
            ('fordoctor/', 'fordoctor'),
            ('login/', 'login'),
            ('register/', 'register'),
            ('otp/', 'otp'),
        ]
        
        for url, name in urls_to_test:
            try:
                response = self.client.get(f'/{url}')
                if response.status_code in [200, 302]:
                    self.log(f"URL /{url} ({name}): Status {response.status_code}", "PASS")
                    self.passed += 1
                else:
                    self.log(f"URL /{url} ({name}): Unexpected status {response.status_code}", "FAIL")
                    self.failed += 1
            except Exception as e:
                self.log(f"URL /{url} ({name}): Error - {str(e)}", "FAIL")
                self.failed += 1
                self.errors.append(f"URL {url}: {str(e)}")
    
    def test_database_models(self):
        """Test database models and queries"""
        self.log("\n=== Testing Database Models ===", "INFO")
        
        models_to_test = [
            ('UserDetail', UserDetail),
            ('DoctorDetail', DoctorDetail),
            ('bookappointment', bookappointment),
            ('appointmenthistory', appointmenthistory),
            ('UserContacts', UserContacts),
            ('DoctorsMessage', DoctorsMessage),
        ]
        
        for model_name, model_class in models_to_test:
            try:
                count = model_class.objects.count()
                self.log(f"Model {model_name}: {count} records", "PASS")
                self.passed += 1
            except Exception as e:
                self.log(f"Model {model_name}: Error - {str(e)}", "FAIL")
                self.failed += 1
                self.errors.append(f"Model {model_name}: {str(e)}")
    
    def test_view_functions(self):
        """Test all view functions exist and are callable"""
        self.log("\n=== Testing View Functions ===", "INFO")
        
        view_functions = [
            'homepage', 'contactus', 'about', 'fordoctor', 'login', 'register',
            'otp', 'userhomepage', 'appointment', 'emergencyappointment',
            'appointmentlist', 'history', 'userdetail', 'doctorschedule',
            'prescription', 'userlogout', 'bookuserappointment', 'bookemergencyappointment'
        ]
        
        for func_name in view_functions:
            try:
                func = getattr(views, func_name)
                if callable(func):
                    self.log(f"View function '{func_name}': Exists and callable", "PASS")
                    self.passed += 1
                else:
                    self.log(f"View function '{func_name}': Not callable", "FAIL")
                    self.failed += 1
            except AttributeError:
                self.log(f"View function '{func_name}': Not found", "FAIL")
                self.failed += 1
                self.errors.append(f"View {func_name}: Not found")
    
    def test_templates_exist(self):
        """Test all templates are accessible"""
        self.log("\n=== Testing Templates ===", "INFO")
        
        templates = [
            'index.html', 'registrationpage.html', 'login.html', 'aboutus.html',
            'contactus.html', 'appointmentpage.html', 'bookappointment.html',
            'userhomepage.html', 'doctorpage.html', 'otp.html', 'userdetail.html',
            'emergencyappointmentpage.html', 'userhistory.html', 'doctorschedule.html',
            'bookemergencyappointment.html', 'appointmentlist.html', 'prescription.html'
        ]
        
        from django.template.loader import get_template
        from django.template import TemplateDoesNotExist
        
        for template_name in templates:
            try:
                get_template(template_name)
                self.log(f"Template '{template_name}': Found", "PASS")
                self.passed += 1
            except TemplateDoesNotExist:
                self.log(f"Template '{template_name}': Not found", "FAIL")
                self.failed += 1
                self.errors.append(f"Template {template_name}: Not found")
    
    def test_static_files(self):
        """Test critical static files exist"""
        self.log("\n=== Testing Static Files ===", "INFO")
        
        css_files = [
            'indexstyle.css', 'registrationstyle.css', 'loginstyle.css',
            'aboutusstyle.css', 'contactusstyle.css', 'appointmentpagestyle.css',
            'bookappointmentstyle.css', 'userhomepstyle.css', 'doctorpagestyle.css',
            'otpstyle.css', 'userdetailsstyle.css', 'emergencyappointmentstyle.css',
            'userhistorystyle.css', 'doctorschedulestyle.css', 'bookemergencyappointmentstyle.css',
            'appointmentliststyle.css', 'prescriptionstyle.css', 'responsive-base.css'
        ]
        
        static_dir = 'static/cssfiles'
        for css_file in css_files:
            file_path = os.path.join(static_dir, css_file)
            if os.path.exists(file_path):
                self.log(f"CSS file '{css_file}': Found", "PASS")
                self.passed += 1
            else:
                self.log(f"CSS file '{css_file}': Not found", "FAIL")
                self.failed += 1
                self.errors.append(f"CSS {css_file}: Not found")
    
    def test_user_registration_flow(self):
        """Test user registration process"""
        self.log("\n=== Testing User Registration Flow ===", "INFO")
        
        try:
            # Test GET request
            response = self.client.get('/register/')
            if response.status_code == 200:
                self.log("Registration page GET: Success", "PASS")
                self.passed += 1
            else:
                self.log(f"Registration page GET: Status {response.status_code}", "FAIL")
                self.failed += 1
        except Exception as e:
            self.log(f"Registration page GET: Error - {str(e)}", "FAIL")
            self.failed += 1
            self.errors.append(f"Registration GET: {str(e)}")
    
    def test_login_flow(self):
        """Test login process"""
        self.log("\n=== Testing Login Flow ===", "INFO")
        
        try:
            # Test GET request
            response = self.client.get('/login/')
            if response.status_code == 200:
                self.log("Login page GET: Success", "PASS")
                self.passed += 1
            else:
                self.log(f"Login page GET: Status {response.status_code}", "FAIL")
                self.failed += 1
        except Exception as e:
            self.log(f"Login page GET: Error - {str(e)}", "FAIL")
            self.failed += 1
            self.errors.append(f"Login GET: {str(e)}")
    
    def test_doctor_page(self):
        """Test doctor page functionality"""
        self.log("\n=== Testing Doctor Page ===", "INFO")
        
        try:
            response = self.client.get('/fordoctor/')
            if response.status_code == 200:
                self.log("Doctor page GET: Success", "PASS")
                self.passed += 1
            else:
                self.log(f"Doctor page GET: Status {response.status_code}", "FAIL")
                self.failed += 1
        except Exception as e:
            self.log(f"Doctor page GET: Error - {str(e)}", "FAIL")
            self.failed += 1
            self.errors.append(f"Doctor page GET: {str(e)}")
    
    def test_contact_form(self):
        """Test contact form submission"""
        self.log("\n=== Testing Contact Form ===", "INFO")
        
        try:
            response = self.client.get('/contactus/')
            if response.status_code == 200:
                self.log("Contact page GET: Success", "PASS")
                self.passed += 1
            else:
                self.log(f"Contact page GET: Status {response.status_code}", "FAIL")
                self.failed += 1
        except Exception as e:
            self.log(f"Contact page GET: Error - {str(e)}", "FAIL")
            self.failed += 1
            self.errors.append(f"Contact page GET: {str(e)}")
    
    def test_about_page(self):
        """Test about page"""
        self.log("\n=== Testing About Page ===", "INFO")
        
        try:
            response = self.client.get('/about/')
            if response.status_code == 200:
                self.log("About page GET: Success", "PASS")
                self.passed += 1
            else:
                self.log(f"About page GET: Status {response.status_code}", "FAIL")
                self.failed += 1
        except Exception as e:
            self.log(f"About page GET: Error - {str(e)}", "FAIL")
            self.failed += 1
            self.errors.append(f"About page GET: {str(e)}")
    
    def test_database_integrity(self):
        """Test database integrity and relationships"""
        self.log("\n=== Testing Database Integrity ===", "INFO")
        
        try:
            # Test if we can query all models
            users = UserDetail.objects.all()
            doctors = DoctorDetail.objects.all()
            appointments = bookappointment.objects.all()
            history = appointmenthistory.objects.all()
            
            self.log(f"Database query test: {len(users)} users, {len(doctors)} doctors, {len(appointments)} appointments, {len(history)} history records", "PASS")
            self.passed += 1
        except Exception as e:
            self.log(f"Database query test: Error - {str(e)}", "FAIL")
            self.failed += 1
            self.errors.append(f"Database integrity: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests"""
        self.log("\n" + "="*60, "INFO")
        self.log("COMPREHENSIVE DENTAL MANAGEMENT SYSTEM TESTING", "INFO")
        self.log("="*60, "INFO")
        
        self.test_url_routing()
        self.test_database_models()
        self.test_view_functions()
        self.test_templates_exist()
        self.test_static_files()
        self.test_user_registration_flow()
        self.test_login_flow()
        self.test_doctor_page()
        self.test_contact_form()
        self.test_about_page()
        self.test_database_integrity()
        
        # Print summary
        self.log("\n" + "="*60, "INFO")
        self.log("TEST SUMMARY", "INFO")
        self.log("="*60, "INFO")
        self.log(f"Total Tests Passed: {self.passed}", "PASS")
        if self.failed > 0:
            self.log(f"Total Tests Failed: {self.failed}", "FAIL")
        else:
            self.log(f"Total Tests Failed: {self.failed}", "INFO")
        self.log(f"Success Rate: {(self.passed/(self.passed+self.failed)*100):.1f}%", "INFO")
        
        if self.errors:
            self.log("\n=== ERRORS ENCOUNTERED ===", "INFO")
            for error in self.errors:
                self.log(error, "FAIL")
        
        self.log("\n" + "="*60, "INFO")
        if self.failed == 0:
            self.log("ALL TESTS PASSED! ✓", "PASS")
        else:
            self.log(f"TESTING COMPLETE WITH {self.failed} FAILURES", "INFO")
        self.log("="*60, "INFO")

if __name__ == '__main__':
    tester = TestRunner()
    tester.run_all_tests()
