from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("",views.homepage,name="home"),
    path("contactus/",views.contactus,name="contact"),
    path("about/",views.about,name="about"),
    path("fordoctor/",views.fordoctor,name="fordoctor"),
    path("login/",views.login,name="login"),
    path("register/",views.register,name="register"),
    path("otp/",views.otp,name="otp"),
    path("userhp/<uemailid>/",views.userhomepage,name="userhp"),
    path("appoitment/<uemailid>/",views.appointment,name="appointment"),
    path("emergencyappoitment/<uemailid>/",views.emergencyappointment,name="emergencyappointment"),
    path("applist/<uemailid>/",views.appointmentlist,name="applist"),
    path("history/<uemailid>/",views.history,name="history"),
    path("userdetail/<uemailid>/",views.userdetail,name="userdetail"),
    path("doctorschedule/<demail>/",views.doctorschedule,name="doctors"),
    path("prescriptionpage/<uemail>/",views.prescription,name="prescription"),
    path("userlogout/",views.userlogout,name="userlogout"),
    path("bookappoitment/<demailid>",views.bookuserappointment,name="bookappointment"),
    path("bookemergencyappoitment/<demailid>",views.bookemergencyappointment,name="bookemergencyappointment"),
    
    # Phase 2: Advanced Features URLs
    path("rate-doctor/<doctor_email>/", views.rate_doctor, name="rate_doctor"),
    path("doctor-profile/<doctor_email>/", views.doctor_profile, name="doctor_profile"),
    path("payment/<int:appointment_id>/", views.process_payment, name="process_payment"),
    path("payment-success/<int:payment_id>/", views.payment_success, name="payment_success"),
    path("download-invoice/<int:payment_id>/", views.download_invoice, name="download_invoice"),
    path("payment-history/<user_email>/", views.payment_history, name="payment_history"),
    path("medical-records/<user_email>/", views.medical_records, name="medical_records"),
    path("add-medical-record/<patient_email>/", views.add_medical_record, name="add_medical_record"),
    path("notifications/", views.notifications, name="notifications"),
    path("mark-notification-read/<int:notification_id>/", views.mark_notification_read, name="mark_notification_read"),
    path("patient-dashboard/<user_email>/", views.patient_dashboard, name="patient_dashboard"),
    path("doctor-dashboard/<doctor_email>/", views.doctor_dashboard, name="doctor_dashboard"),
    
    # Phase 3: Advanced Appointment Management URLs
    path("create-recurring-appointment/<doctor_email>/", views.create_recurring_appointment, name="create_recurring_appointment"),
    path("reschedule-appointment/<int:appointment_id>/", views.reschedule_appointment, name="reschedule_appointment"),
    path("join-waitlist/<doctor_email>/", views.join_waitlist, name="join_waitlist"),
    path("create-treatment-plan/<patient_email>/", views.create_treatment_plan, name="create_treatment_plan"),
    path("view-treatment-plans/<user_email>/", views.view_treatment_plans, name="view_treatment_plans"),
    path("treatment-plan-details/<int:plan_id>/", views.treatment_plan_details, name="treatment_plan_details"),
    path("mark-no-show/<int:appointment_id>/", views.mark_no_show, name="mark_no_show"),
    
    # Phase 4: Two-Factor Authentication URLs
    path("enable-2fa/", views.enable_2fa_view, name="enable_2fa_view"),
    path("disable-2fa/", views.disable_2fa_view, name="disable_2fa_view"),
    path("request-2fa-otp/", views.request_2fa_otp, name="request_2fa_otp"),
    path("verify-2fa/", views.verify_2fa_view, name="verify_2fa_view"),
    
    # Phase 4: Advanced Search URL
    path("advanced-search/", views.advanced_search, name="advanced_search"),
    
    # Phase 5: Reports & Analytics URLs
    path("generate-report/", views.generate_report_view, name="generate_report"),
    path("view-reports/", views.view_reports, name="view_reports"),
    path("analytics-dashboard/", views.analytics_dashboard, name="analytics_dashboard"),
    path("export-data/", views.export_data_view, name="export_data"),
    path("export-appointments-csv/", views.export_appointments_csv, name="export_appointments_csv"),
    path("export-payments-csv/", views.export_payments_csv, name="export_payments_csv"),
    path("export-medical-records-csv/", views.export_medical_records_csv, name="export_medical_records_csv"),
    
    # Phase 5: Analytics API Endpoints
    path("api/revenue-analytics/", views.api_revenue_analytics, name="api_revenue_analytics"),
    path("api/appointment-trends/", views.api_appointment_trends, name="api_appointment_trends"),
    path("api/doctor-performance/", views.api_doctor_performance, name="api_doctor_performance"),
    
    # PWA Offline Page
    path("offline/", views.offline_page, name="offline_page"),
]
